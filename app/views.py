from flask import render_template, request
from app import app


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

@app.route("/get-in-touch/contact-us", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        number = request.form["number"]
        message = request.form["message"]
        print(f"{name} \n {email} \n {number} \n {message}")

    else:
        return render_template("public/contact.html")

@app.route("/get-in-touch/volunteers", methods=["GET", "POST"])
def volunteer():
    if request.method == "POST":
        vol_name = request.form["vol_name"]
        vol_email = request.form["vol_email"]
        vol_number = request.form["vol_number"]
        vol_organization = request.form["vol_organization"]
        vol_text = request.form["vol_text"]
        print(f"{vol_name} \n {vol_email} \n {vol_organization} \n {vol_text}")
    else:
        return render_template("public/volunteer.html")

@app.route("/get-in-touch/partners", methods=["GET", "POST"])
def partners():
    if request.method == "POST":
        part_name = request.form["part_name"]
        part_email = request.form["part_email"]
        part_number = request.form["part_number"]
        part_organization = request.form["part_organization"]
        part_text = request.form["part_text"]
        print(f"{part_name} \n {part_email} \n {part_number} \n {part_organization} \n {part_text}")
        
    else:
        return render_template("public/partners.html")

@app.route("/donation", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        pass
    else:
        return render_template("public/donation.html")

@app.route("/donation/paystack")
def paystack():
    return render_template("public/paystack.html")
