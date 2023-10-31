import time

from app import *

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

admin = Admin(app, name="HTP!m Admin Interface", template_mode="bootstrap3")

class AdminModelView(ModelView):

	def is_accessible(self):
		return current_user.is_authenticated and current_user.username == "admin"

	def inaccessible_callback(self, name, **kwargs):
		# Redirect to login page if user doesn't have access.
		return redirect(url_for("login", next=request.url))

admin.add_view(AdminModelView(Team, db.session))
admin.add_view(AdminModelView(Player, db.session))
admin.add_view(AdminModelView(Challenge, db.session))
admin.add_view(AdminModelView(Solve, db.session))

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
	return redirect(url_for("login"))

