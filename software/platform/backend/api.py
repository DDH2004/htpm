from app import *

@app.route("/api/manage/teams", methods=["POST"])
def post_teams():

	# {"action": "create", "name": foo, "password": bar}

	team = Team(request.form["name"], request.form["password"])
	db.session.add(team)
	db.session.commit()
	return {"Status": "Success!"}, 200

@app.route("/api/manage/teams", methods=["GET"])
def get_teams():

	results = Team.query.all()
	print(reults)
