import time

from app import *

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_login import LoginManager, login_required, login_user, logout_user

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Team, db.session))

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

@loginManager.user_loader
def load_user(id: int):
	return Team.query.get(id)

@app.route("/login", methods=["POST"])
def login():

	assert "username" in request.form.keys() and "password" in request.form.keys()
	team = Team.login(request.form["username"], request.form["password"])

	if team == None:
		time.sleep(1)  # Prevent brute.
		return render_template("login.html", failed=True)

	login_user(team)
	return redirect(url_for("application"))

@app.route("/logout", methods=["GET"])
@login_required
def logout():

	logout_user()
	return render_template("index.html")

