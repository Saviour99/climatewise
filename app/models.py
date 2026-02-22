from app import db
from datetime import datetime, timezone


class ContactMessage(db.Model):
    __tablename__ = "contact_message"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self):
        return f"<ContactMessage {self.name} - {self.email}>"


class VolunteerApplication(db.Model):
    __tablename__ = "volunteer_applications"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, index=True)
    number = db.Column(db.String(20), nullable=False)
    organization = db.Column(db.String(200))
    message = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self):
        return f"<VolunteerApplication {self.name} - {self.email}>"


class PartnerApplication(db.Model):
    __tablename__ = "partner_applications"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, index=True)
    number = db.Column(db.String(20), nullable=False)
    organization = db.Column(db.String(200))
    message = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self):
        return f"<PartnerApplication {self.name} - {self.email}>"


class Admin(db.Model):
    """
    Two main roles:
      - 'developer' : (Saviour) — full access, can see all data
      - 'ceo'       : Company CEO — full access
      - 'admin'     : Standard admin (for future use)

    Both developer and CEO see exactly the same dashboard.
    Disable an account without deleting: set is_active_account = False.
    """
    __tablename__ = "admins"

    ROLE_DEVELOPER = 'developer'
    ROLE_CEO       = 'ceo'
    ROLE_ADMIN     = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(30), default='admin', nullable=False)
    is_active_account = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Flask-Login interface
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.is_active_account

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # Role helpers
    @property
    def is_developer(self):
        return self.role == self.ROLE_DEVELOPER

    @property
    def is_ceo(self):
        return self.role == self.ROLE_CEO

    @property
    def is_super_admin(self):
        """Developer and CEO both have full access."""
        return self.role in (self.ROLE_DEVELOPER, self.ROLE_CEO)

    @property
    def role_label(self):
        return {
            'developer': 'Developer',
            'ceo': 'Chief Executive Officer',
            'admin': 'Administrator',
        }.get(self.role, 'Administrator')

    def __repr__(self):
        return f"<Admin {self.name} [{self.role}]>"


class Donation(db.Model):
    """
    Paystack donations.
    Only rows where is_verified=True count in dashboard totals.
    is_anonymous=True hides donor name on public-facing display.
    """
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)

    donor_name = db.Column(db.String(150), nullable=False)
    donor_email = db.Column(db.String(150), nullable=False, index=True)
    is_anonymous = db.Column(db.Boolean, default=False)

    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(10), default='GHS')

    paystack_reference = db.Column(db.String(200), unique=True, nullable=False, index=True)
    paystack_status = db.Column(db.String(50), default='pending')
    is_verified = db.Column(db.Boolean, default=False, index=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Donation {self.donor_name} GH₵{self.amount} [{self.paystack_status}]>"