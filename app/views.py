from flask import render_template
from app import app


@app.route("/")
@app.route("/home")
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

@app.route("/thematic/research-innovation-and-policy advocacy")
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

@app.route("/touch/contact-us")
def contact():
    return render_template("public/contact.html")

@app.route("/touch/volunteers")
def volunteer():
    return render_template("public/volunteer.html")

@app.route("/touch/partners")
def partners():
    return render_template("public/partners.html")

@app.route("/donation")
def donate():
    return render_template("public/donate.html")

@app.route("/donation/paystack")
def paystack():
    return render_template("public/paystack.html")
