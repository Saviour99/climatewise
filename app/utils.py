import bleach
import re

def sanitize_text(value):
    """Remove all HTML tags and dangerous content"""
    if not value:
        return ""
    return bleach.clean(value.strip(), tags=[], strip=True)

def sanitize_email(value):
    """Validate and clean email format"""
    if not value:
        return ""
    cleaned = bleach.clean(value.strip(), tags=[], strip=True)
    # Basic email format check
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, cleaned):
        return None  # signals invalid email
    return cleaned

def sanitize_phone(value):
    """Only allow numbers, +, spaces, dashes"""
    if not value:
        return ""
    # Strips everything except valid phone characters
    return re.sub(r'[^\d\+\-\s\(\)]', '', value.strip())