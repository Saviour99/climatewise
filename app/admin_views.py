from flask import render_template
from app import app


@app.route("/admin/dashboard")
def admin():
    return render_template("admin/dashboard.html")
