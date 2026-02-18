from flask import Flask
from flask_mail import Mail
import os
import dotenv


dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Mail Configurations
app.config["MAIL_SERVER"] = "smtp.sendgrid.net"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "apikey"
app.config["MAIL_PASSWORD"] = os.getenv("SENDGRID_API")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("USER_EMAIL")

mail = Mail(app)

from app import models
from app import views
from app import config
from app import forms
