from app import *

@app.route("/api/manage/teams", methods=["POST"])
def post_teams():

	if request.form["action"] == "create":
		try:
			team = Team(request.form["name"], request.form["password"])
			db.session.add(team)
			db.session.commit()
		except:
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "update":
		try:
			team = Team.query.filter_by(name=request.form["name"]).first()
			team.name = request.form["newName"]
			team.password = bcrypt.hashpw(request.form["newPassword"].encode(), bcrypt.gensalt(4))
			db.session.add(team)
			db.session.commit()
		except:
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "delete":
		try:
			team = Team.query.filter_by(name=request.form["name"]).first()
			db.session.delete(team)
			db.session.commit()
		except:
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	return {"Status": "Failure."}, 400

@app.route("/api/manage/teams", methods=["GET"])
def get_teams():

	results = [t.name for t in Team.query.all()]
	return {"Status": "Success!", "Teams": results}, 200

@app.route("/api/manage/players", methods=["POST"])
def post_players():

	if request.form["action"] == "create":
		try:
			player = Player(request.form["team"], request.form["name"])
			db.session.add(player)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "update":
		try:
			player = Player.query.filter_by(team=request.form["team"], name=request.form["name"]).first()
			player.team = request.form["newTeam"]
			player.name = request.form["newName"]
			db.session.add(player)
			db.session.commit()
		except:
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "delete":
		try:
			player = Player.query.filter_by(team=request.form["team"], name=request.form["name"]).first()
			db.session.delete(player)
			db.session.commit()
		except:
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	return {"Status": "Failure."}, 400

@app.route("/api/manage/players", methods=["GET"])
def get_players():

	results = [f"{p.team} {p.name}" for p in Player.query.all()]
	return {"Status": "Success!", "Teams": results}, 200

