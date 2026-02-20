from flask import render_template, request, redirect, url_for, flash
from app import app, mail, db
from app.models import ContactMessage, VolunteerApplication, PartnerApplication
from app.utils import sanitize_text, sanitize_email, sanitize_phone
from flask_wtf.csrf import CSRFError
from flask_mail import Message
import os
import dotenv
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print(f"✅ Email sent successfully")
        except Exception as e:
            print(f"❌ Error sending email: {e}")

@app.route("/")
def home():
    return render_template("public/home.html")

@app.route("/about/who-we-are")
def about():
    return render_template("public/about.html")

@app.route("/about/team")
def teams():
    return render_template("public/teams.html")

@app.route("/thematic/climate-resilience-and-adaptation")
def climate():
    return render_template("public/climate.html")

@app.route("/thematic/water-sanitation-and-hygiene")
def water():
    return render_template("public/water.html")

@app.route("/thematic/environmental-sustainability-circuar-economy-and-waste-management")
def environment():
    return render_template("public/environment.html")

@app.route("/thematic/youth-empowerment-and-capacity-building")
def youth():
    return render_template("public/youth.html")

@app.route("/thematic/climate-education-and-public-awareness")
def education():
    return render_template("public/education.html")

@app.route("/thematic/research-innovation-and-policy-advocacy")
def research():
    return render_template("public/research.html")

@app.route("/projects-and-impacts")
def projects():
    return render_template("public/projects.html")

@app.route("/media")
def media():
    return render_template("public/media.html")

@app.route("/resources/news-and-updates")
def news():
    return render_template("public/news.html")

@app.route("/resources/publications")
def publications():
    return render_template("public/publications.html")

@app.route("/get-in-touch/contact-us")
def contact():
    return render_template("public/contact.html")

@app.route("/get-in-touch/contact-us/sending-mail", methods=["GET", "POST"])
def send_mail():
    if request.method == "POST":
        name = sanitize_text(request.form.get("name", ""))
        email = sanitize_email(request.form.get("email", ""))
        number = sanitize_phone(request.form.get("number", ""))
        message = sanitize_text(request.form.get("message", ""))
        subject = "ClimateWISE Youth Organization"
        print(f"{name} \n {email} \n {number} \n {message}")

        # Form Data Validation
        if not all([name, email, number, subject, message]):
            flash("All fields are required", category="error")
            return redirect(url_for("contact"))
       
        try:
            # Sending the mail
            msg = Message(
                subject,
                sender=os.getenv("USER_EMAIL"),
                recipients=[os.getenv("USER_EMAIL"), "saviourb100@gmail.com"]
            )
            msg.body = f"Message from: {name}\nEmail: {email}\nPhone Number: {number}\nSubject: {subject}\n\nDescription: {message}"
            
            # Send email in background thread
            Thread(target=send_async_email, args=(app, msg)).start()

            #Save to the database
            new_message = ContactMessage(
                name=name,
                email=email,
                number=number,
                message=message
            )
            db.session.add(new_message)
            db.session.commit()
            
            flash("Message sent successfully!", category="success")
        except Exception as e:
            db.session.rollback()
            print(f"Error sending email: {e}")
            flash("Failed to send message. Please try again later.", category="error")
        return redirect(url_for("contact"))

@app.route("/get-in-touch/volunteers")
def volunteer():
    return render_template("public/volunteer.html")

@app.route("/get-in-touch/volunteers/sending-details", methods=["POST"])
def send_details():
    vol_name = sanitize_text(request.form.get("vol_name", ""))
    vol_email = sanitize_email(request.form.get("vol_email", ""))
    vol_number = sanitize_phone(request.form.get("vol_number", ""))
    vol_organization = sanitize_text(request.form.get("vol_organization", ""))
    vol_text = sanitize_text(request.form.get("vol_text", ""))
    print(f"{vol_name} \n{vol_email} \n{vol_organization} \n{vol_number} \n{vol_text}")

    if not all([vol_name, vol_email, vol_number]):
        flash("Name, email and phone number are required.", category="error")
        return redirect(url_for("volunteer"))

    try:
        #Save to the database
        new_volunteer = VolunteerApplication(
            name=vol_name,
            email=vol_email,
            number=vol_number,
            organization=vol_organization,
            message=vol_text
        )
        db.session.add(new_volunteer)
        db.session.commit()

        flash("Application sent successfully!", category="success")

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        flash("Something went wrong. Please try again later.", category="error")

    return redirect(url_for("volunteer"))

@app.route("/get-in-touch/partners")
def partners():
    return render_template("public/partners.html")

@app.route("/get-in-touch/partners/sending-details", methods=["POST"])
def send_detail():    
    part_name = sanitize_text(request.form.get("part_name", ""))
    part_email = sanitize_email(request.form.get("part_email", ""))
    part_number = sanitize_phone(request.form.get("part_number", ""))
    part_organization = sanitize_text(request.form.get("part_organization", ""))
    part_text = sanitize_text(request.form.get("part_text", ""))
    print(f"{part_name} \n{part_email} \n{part_number} \n{part_organization} \n{part_text}")
    
    if not all([part_name, part_email, part_number]):
        flash("Name, email and phone number are required.", category="error")
        return redirect(url_for("partners"))

    try:
        #Save to the database
        new_partner = PartnerApplication(
            name=part_name,
            email=part_email,
            number=part_number,
            organization=part_organization,
            message=part_text
        )
        db.session.add(new_partner)
        db.session.commit()

        flash("Application sent successfully!", category="success")

    except Exception as e:
        db.session.rollback()
        print(f"Error sending email: {e}")
        flash("Failed to send message. Please try again later.", category="error")

    return redirect(url_for("partners"))

@app.route("/donation", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        pass
    else:
        return render_template("public/donation.html")

@app.route("/donation/paystack")
def paystack():
    return render_template("public/paystack.html")

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash("Session expired. Please try submitting the form again.", category="error")
    return redirect(request.referrer or url_for("home"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", 404)

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", 500)