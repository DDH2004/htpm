from app import *

from flask_login import current_user, login_required

@app.route("/", methods=["GET"])
def index():

	return render_template("splash.html")

@app.route("/login", methods=["GET"])
def loginPage():

	if current_user.is_authenticated:
		return redirect(url_for("application"))

	return render_template("login.html")

@app.route("/app", methods=["GET"])
@login_required
def application():

	if current_user.username == "admin":
		return redirect("/admin")

	return render_template("home.html")

