from flask import Flask
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["WTF_CSRF_ENABLED"] = True

# Mail Configurations
# app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'api'
# app.config['MAIL_PASSWORD'] = os.getenv('MAILTRAP_API')
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv('USER_EMAIL')

# sending emails in production by using mailtrap sandbox
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWRD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAM')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

mail = Mail(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# ---- Custom template filters ----
@app.template_filter('milestone')
def milestone_filter(n):
    milestones = [10, 50, 100, 150, 200, 250, 500, 1000, 2000]
    n = int(n or 0)
    if n < 10:
        return str(n)
    reached = 0
    for m in milestones:
        if n >= m:
            reached = m
        else:
            break
    return f"{reached}+"

from app import models, views, utils, config, forms
from app import admin_views