from flask import render_template
from app import app


@app.route("/")
@app.route("/home")
def homepage():
    return render_template("public/home.html")

@app.route("/about/who-we-are")
def about():
    return render_template("about.html")

@app.route("/about/team")
def teams():
    return render_template("teams.html")

@app.route("/thematic/climate-resilience-and-adaptation")
def climate():
    return render_template("climate.html")

@app.route("/thematic/water-sanitation-and-hygiene")
def water():
    return render_template("water.html")

@app.route("/thematic/environmental-sustainability-circuar-economy-and-waste-management")
def environment():
    return render_template("environment.html")

@app.route("/thematic/youth-empowerment-and-capacity-building")
def youth():
    return render_template("youth.html")

@app.route("/thematic/climate-education-and-public-awareness")
def education():
    return render_template("education.html")

@app.route("/thematic/research-innovation-and-policy advocacy")
def research():
    return render_template("research.html")

@app.route("/projects-and-impacts")
def projects():
    return render_template("projects.html")

@app.route("/media")
def media():
    return render_template("media.html")

@app.route("/resources/news-and-updates")
def news():
    return render_template("news.html")

@app.route("/resources/publications")
def publications():
    return render_template("publications.html")

@app.route("/touch/contact-us")
def contact():
    return render_template("contact.html")

@app.route("/touch/volunteers")
def volunteer():
    return render_template("volunteer.html")

@app.route("/touch/partners")
def partners():
    return render_template("partners.html")

