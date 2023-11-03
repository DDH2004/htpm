from app import *

@app.route("/api/lights/disable", methods=["POST"])
@login_required
def disable_lights():

	with open("./states/lights.txt", "w") as f:
		f.write("0\n")

	return redirect(url_for("application"))

@app.route("/api/notes/update", methods=["POST"])
@login_required
def update_notes():

	with open("./states/notes.txt", "w") as f:
		f.write(request.form["notes"]+"\n")

	return redirect(url_for("application"))

@app.route("/api/lights/enable", methods=["POST"])
@login_required
def enable_lights():

	with open("./states/lights.txt", "w") as f:
		f.write("1\n")

	return redirect(url_for("application"))

