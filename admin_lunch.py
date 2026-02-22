from app import app, db
from app.models import Admin
from werkzeug.security import generate_password_hash
import os 
import dotenv


dotenv.load_dotenv()

DEVELOPER = {
    'name': os.getenv("DEV_NAME"),
    'email': os.getenv("DEV_EMAIL"),
    'password': os.getenv("DEV_PASSWORD"),
    'role': Admin.ROLE_DEVELOPER,
}

CEO = {
    'name': os.getenv("ADMIN_NAME"),
    'email': os.getenv("ADMIN_EMAIL"),
    'password': os.getenv("ADMIN_PASSWORD"),
    'role': Admin.ROLE_CEO,
}

def create_admin(data: dict):
    existing = Admin.query.filter_by(email=data['email']).first()
    if existing:
        print(f"⚠️  Account already exists for {data['email']} — skipping.")
        return

    admin = Admin(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        role=data['role'],
        is_active_account=True,
    )
    db.session.add(admin)
    db.session.commit()
    print(f"✅ Created [{data['role'].upper()}] account: {data['name']} ({data['email']})")


with app.app_context():
    create_admin(DEVELOPER)
    create_admin(CEO)
    print("Accounts created successfully")