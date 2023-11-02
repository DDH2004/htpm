from app import *

@app.route("/api/lights/disable", methods=["POST"])
@login_required
def disable_lights():

	with open("./states/lights.txt", "w") as f:
		f.write("0")

	return redirect(url_for("application"))

@app.route("/api/notes/update", methods=["POST"])
@login_required
def update_notes():

	with open("./states/notes.txt", "w") as f:
		f.write(request.form["notes"])

	return redirect(url_for("application"))
