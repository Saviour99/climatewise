import re
import os
import hmac
import hashlib
from datetime import datetime, timezone, timedelta

from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from sqlalchemy import func

from app import app, db
from app.models import Admin, VolunteerApplication, PartnerApplication, Donation, ContactMessage
from app.utils import rate_limit, sanitize_email, sanitize_amount, sanitize_text, sanitize_phone, add_security_headers

# ---- Apply security headers to EVERY response ----
app.after_request(add_security_headers)

# ---- Flask-Login setup ----
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Please sign in to access the admin panel.'
login_manager.login_message_category = 'error'


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


# ============================================================
# HELPERS
# ============================================================

def time_ago(dt: datetime) -> str:
    if dt is None:
        return ''
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    seconds = int((now - dt).total_seconds())
    if seconds < 60:
        return 'Just now'
    elif seconds < 3600:
        m = seconds // 60
        return f'{m} minute{"s" if m > 1 else ""} ago'
    elif seconds < 86400:
        h = seconds // 3600
        return f'{h} hour{"s" if h > 1 else ""} ago'
    elif seconds < 604800:
        d = seconds // 86400
        return f'{d} day{"s" if d > 1 else ""} ago'
    return dt.strftime('%b %d, %Y')


def get_unique_member_count() -> int:
    """
    Count unique people across volunteers AND partners by email.
    If someone registers as both a volunteer AND a partner,
    they count as 1 member — not 2.
    Uses SQL UNION which removes duplicates automatically.
    """
    volunteer_emails = db.session.query(
        func.lower(VolunteerApplication.email)
    ).distinct()

    partner_emails = db.session.query(
        func.lower(PartnerApplication.email)
    ).distinct()

    all_unique = volunteer_emails.union(partner_emails).all()
    return len(all_unique)


def build_activity_feed(limit: int = 15) -> list:
    activities = []

    for v in VolunteerApplication.query.order_by(
            VolunteerApplication.date_created.desc()).limit(limit).all():
        activities.append({
            'type': 'volunteer',
            'text': f'{v.name} signed up as a volunteer',
            'time_ago': time_ago(v.date_created),
            'dt': v.date_created
        })

    for p in PartnerApplication.query.order_by(
            PartnerApplication.date_created.desc()).limit(limit).all():
        activities.append({
            'type': 'partner',
            'text': f'{p.name} ({p.organization or "Individual"}) registered as a partner',
            'time_ago': time_ago(p.date_created),
            'dt': p.date_created
        })

    for d in Donation.query.filter_by(is_verified=True).order_by(
            Donation.created_at.desc()).limit(limit).all():
        display_name = 'Anonymous' if d.is_anonymous else d.donor_name
        activities.append({
            'type': 'donation',
            'text': f'{display_name} donated GH₵{d.amount:,.2f}',
            'time_ago': time_ago(d.created_at),
            'dt': d.created_at
        })

    for m in ContactMessage.query.order_by(
            ContactMessage.date_created.desc()).limit(limit).all():
        activities.append({
            'type': 'message',
            'text': f'{m.name} sent a message',
            'time_ago': time_ago(m.date_created),
            'dt': m.date_created
        })

    activities.sort(
        key=lambda x: x['dt'] if x['dt'].tzinfo else x['dt'].replace(tzinfo=timezone.utc),
        reverse=True
    )
    return activities[:limit]


def get_donation_chart_data():
    """Last 6 months of verified donation totals for Chart.js."""
    now = datetime.now(timezone.utc)
    labels, data = [], []
    for i in range(5, -1, -1):
        month_start = (now.replace(day=1) - timedelta(days=i * 30)).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (month_start + timedelta(days=32)).replace(day=1) if i > 0 else now
        total = db.session.query(func.coalesce(func.sum(Donation.amount), 0)).filter(
            Donation.is_verified == True,
            Donation.created_at >= month_start,
            Donation.created_at < next_month
        ).scalar()
        labels.append(month_start.strftime('%b %Y'))
        data.append(float(total))
    return labels, data


def sidebar_context() -> dict:
    return {
        'volunteer_count': VolunteerApplication.query.count(),
        'partner_count': PartnerApplication.query.count(),
    }


# ============================================================
# ADMIN AUTH
# ============================================================

@app.route('/admin/login', methods=['GET', 'POST'])
@rate_limit(max_requests=10, window=60)  # 10 attempts/min per IP — blocks brute force
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        email = sanitize_email(request.form.get('email', ''))
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please enter both email and password.', 'error')
            return redirect(url_for('admin_login'))

        admin = Admin.query.filter_by(email=email).first()

        # Always run check_password_hash even when admin is None
        # This prevents timing attacks that reveal valid emails
        dummy_hash = 'pbkdf2:sha256:260000$x$x'
        valid = check_password_hash(
            admin.password if admin else dummy_hash,
            password
        ) and admin is not None

        if not valid:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('admin_login'))

        if not admin.is_active_account:
            flash('This account has been disabled. Contact the system administrator.', 'error')
            return redirect(url_for('admin_login'))

        admin.last_login = datetime.now(timezone.utc)
        db.session.commit()

        remember = bool(request.form.get('remember'))
        login_user(admin, remember=remember)

        # Prevent open-redirect attacks — only allow relative paths
        next_page = request.args.get('next')
        if next_page and not next_page.startswith('/'):
            next_page = None

        return redirect(next_page or url_for('admin_dashboard'))

    stats = {
        'total_members': get_unique_member_count(),
        'total_donations': Donation.query.filter_by(is_verified=True).count()
    }
    return render_template('admin/login.html', stats=stats)


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been signed out.', 'success')
    return redirect(url_for('admin_login'))


# ============================================================
# ADMIN DASHBOARD & PAGES
# ============================================================

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_volunteers = VolunteerApplication.query.count()
    total_partners = PartnerApplication.query.count()
    total_members = get_unique_member_count()
    total_donations_amount = db.session.query(
        func.coalesce(func.sum(Donation.amount), 0)
    ).filter(Donation.is_verified == True).scalar()

    recent_activities = build_activity_feed(limit=12)
    donation_labels, donation_data = get_donation_chart_data()

    return render_template(
        'admin/dashboard.html',
        total_volunteers=total_volunteers,
        total_partners=total_partners,
        total_members=total_members,
        total_donations_amount=float(total_donations_amount),
        recent_activities=recent_activities,
        donation_labels=donation_labels,
        donation_data=donation_data,
        **sidebar_context()
    )


@app.route('/admin/api/activity')
@login_required
def admin_api_activity():
    activities = build_activity_feed(limit=12)
    for a in activities:
        a.pop('dt', None)
    return jsonify({'activities': activities})


@app.route('/admin/volunteers')
@login_required
def admin_volunteers():
    page = request.args.get('page', 1, type=int)
    volunteers = VolunteerApplication.query.order_by(
        VolunteerApplication.date_created.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/volunteers.html', volunteers=volunteers, **sidebar_context())


@app.route('/admin/partners')
@login_required
def admin_partners():
    page = request.args.get('page', 1, type=int)
    partners = PartnerApplication.query.order_by(
        PartnerApplication.date_created.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/partners.html', partners=partners, **sidebar_context())


@app.route('/admin/donations')
@login_required
def admin_donations():
    page = request.args.get('page', 1, type=int)
    donations = Donation.query.filter_by(is_verified=True).order_by(
        Donation.created_at.desc()
    ).paginate(page=page, per_page=20)
    total = db.session.query(func.coalesce(func.sum(Donation.amount), 0)).filter(
        Donation.is_verified == True
    ).scalar()
    return render_template(
        'admin/donations.html',
        donations=donations,
        total=float(total),
        **sidebar_context()
    )


@app.route('/admin/messages')
@login_required
def admin_messages():
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(
        ContactMessage.date_created.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/messages.html', messages=messages, **sidebar_context())