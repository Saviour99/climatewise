from flask import Flask, render_template


app = Flash(__name__)

@app.route("/")
@app.route("/home/")
def homepage:
    return render_template("")

@app.route("/about/")
def homepage:
    return render_template("")

@app.route("/about/")
def homepage:
    return render_template("")

@app.route("/thematic/")
def homepage:
    return render_template("")

@app.route("/projects")
def homepage:
    return render_template("")

@app.route("/media")
def homepage:
    return render_template("")

@app.route("/resources")
def homepage:
    return render_template("")

@app.route("/touch")
def homepage:
    return render_template("")


if __name__ == "__main__":
    app.run(debug=True)