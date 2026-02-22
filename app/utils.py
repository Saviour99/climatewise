import bleach
import re
import time
from functools import wraps
from flask import request, abort, Response


# ============================================================
# INPUT SANITIZATION
# ============================================================

def sanitize_text(value: str) -> str:
    """Strip all HTML tags and dangerous characters."""
    if not value:
        return ""
    return bleach.clean(str(value).strip(), tags=[], strip=True)[:500]


def sanitize_email(value: str):
    """Validate and sanitize an email address. Returns None if invalid."""
    if not value:
        return None
    cleaned = bleach.clean(str(value).strip().lower(), tags=[], strip=True)
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, cleaned) or len(cleaned) > 150:
        return None
    return cleaned


def sanitize_phone(value: str) -> str:
    """Allow only valid phone number characters."""
    if not value:
        return ""
    return re.sub(r'[^\d\+\-\s\(\)]', '', str(value).strip())[:20]


def sanitize_amount(value) -> float | None:
    """
    Validate donation amount.
    Must be between GH₵1 and GH₵100,000.
    Returns None if invalid.
    """
    try:
        amount = float(str(value).strip())
        if amount < 1 or amount > 100_000:
            return None
        return round(amount, 2)
    except (ValueError, TypeError):
        return None


# ============================================================
# RATE LIMITING
# In-memory store — resets on server restart.
# For production with multiple workers, use flask-limiter + Redis.
# ============================================================

_rate_store: dict = {}


def is_rate_limited(ip: str, max_requests: int = 10, window: int = 60) -> bool:
    """Return True if the IP has exceeded the allowed request rate."""
    now = time.time()
    timestamps = [t for t in _rate_store.get(ip, []) if now - t < window]
    _rate_store[ip] = timestamps
    if len(timestamps) >= max_requests:
        return True
    _rate_store[ip].append(now)
    return False


def rate_limit(max_requests: int = 10, window: int = 60):
    """
    Route decorator — blocks excessive requests from the same IP.
    Returns HTTP 429 when limit is exceeded.

    Usage:
        @app.route('/admin/login', methods=['GET', 'POST'])
        @rate_limit(max_requests=10, window=60)
        def admin_login(): ...
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Handle proxy headers (e.g. Nginx, Heroku)
            ip = request.headers.get('X-Forwarded-For', request.remote_addr or '0.0.0.0')
            ip = ip.split(',')[0].strip()
            if is_rate_limited(ip, max_requests, window):
                abort(429)
            return f(*args, **kwargs)
        return wrapped
    return decorator


# ============================================================
# SECURITY HEADERS
# Register in __init__.py ONCE:
#   from app.utils import add_security_headers
#   app.after_request(add_security_headers)
# ============================================================

def add_security_headers(response: Response) -> Response:
    """
    Apply HTTP security headers to every response.

    Protects against:
    - Clickjacking          (X-Frame-Options)
    - MIME sniffing         (X-Content-Type-Options)
    - XSS                   (X-XSS-Protection + CSP)
    - Information leakage   (Referrer-Policy)
    - Unwanted features     (Permissions-Policy)
    - Mixed content         (CSP)
    """
    h = response.headers

    h['X-Frame-Options'] = 'SAMEORIGIN'
    h['X-Content-Type-Options'] = 'nosniff'
    h['X-XSS-Protection'] = '1; mode=block'
    h['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    h['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

    # Uncomment when deployed on HTTPS:
    # h['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # Content Security Policy — allows Bootstrap CDN, FontAwesome,
    # Google Fonts, Chart.js, Paystack JS, and your own static files.
    h['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net "
            "https://cdnjs.cloudflare.com "
            "https://kit.fontawesome.com "
            "https://js.paystack.co; "
        "style-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net "
            "https://cdnjs.cloudflare.com "
            "https://fonts.googleapis.com; "
        "font-src 'self' "
            "https://fonts.gstatic.com "
            "https://cdnjs.cloudflare.com "
            "https://ka-f.fontawesome.com; "
        "img-src 'self' data: https: blob:; "
        "connect-src 'self' https://api.paystack.co; "
        "frame-src https://js.paystack.co; "
        "object-src 'none'; "
        "base-uri 'self';"
    )

    # Admin pages must never be cached — prevents sensitive data
    # appearing in browser back-button history
    if '/admin' in request.path:
        h['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        h['Pragma'] = 'no-cache'
        h['Expires'] = '0'

    return response