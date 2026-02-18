from flask import render_template, request, redirect, url_for, flash
from app import app, mail
from flask_mail import Message
import os
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
        name = request.form["name"]
        email = request.form["email"]
        number = request.form["number"]
        message = request.form["message"]
        subject = "ClimateWISWE Youth Organization"
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
            msg.body = f"Message from: {name}\nEmail: {email}\Phone Number: {number}\nSubject: {subject}\n\nDescription: {message}"
            
            # Send email in background thread
            Thread(target=send_async_email, args=(app, msg)).start()
            
            flash("Message sent successfully!", category="success")
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("Failed to send message. Please try again later.", category="error")
        return redirect(url_for("contact"))

@app.route("/get-in-touch/volunteers")
def volunteer():
    return render_template("public/volunteer.html")


@app.route("/get-in-touch/volunteers/sending-details", methods=["GET","POST"])
def send_details():
    if request.method == "POST":
        vol_name = request.form["vol_name"]
        vol_email = request.form["vol_email"]
        vol_number = request.form["vol_number"]
        vol_organization = request.form["vol_organization"]
        vol_text = request.form["vol_text"]
        print(f"{vol_name} \n{vol_email} \n{vol_organization} \n{vol_number} \n{vol_text}")
        flash("Message sent successfully!", category="success")
        return redirect(url_for("volunteer"))

@app.route("/get-in-touch/partners")
def partners():
    return render_template("public/partners.html")

@app.route("/get-in-touch/partners/sending-details", methods=["GET", "POST"])
def send_detail():
    if request.method == "POST":
        part_name = request.form["part_name"]
        part_email = request.form["part_email"]
        part_number = request.form["part_number"]
        part_organization = request.form["part_organization"]
        part_text = request.form["part_text"]
        print(f"{part_name} \n{part_email} \n{part_number} \n{part_organization} \n{part_text}")
        flash("Message sent successfully!", category="success")
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
