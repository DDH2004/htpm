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



@app.route("/api/manage/challenges", methods=["POST"])
def post_challenges():

	if request.form["action"] == "create":
		print(request.form) 
		try:
			challenge = Challenge(request.form["points"], request.form["title"], request.form["instructions"])
			db.session.add(challenge)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure. create error"}, 400
		return {"Status": "Success!"}, 200
		
	elif request.form["action"] == "update":
		try:
			challenge = Challenge.query.filter_by(points=request.form["points"], title=request.form["title"], instructions=request.form["instructions"]).first()
			if not challenge:
				return {"Status": "Failure. Challenge not found"}, 404
			
			challenge.points = request.form["newPoints"]
			challenge.title = request.form["newTitle"]
			challenge.instructions = request.form["newInstructions"]
			db.session.add(challenge)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure. update error"}, 400
		return {"Status": "Success!"}, 200
	
	elif request.form["action"] == "delete":
		try:
			challenge = Challenge.query.filter_by(points=request.form["points"], title=request.form["title"], instructions=request.form["instructions"]).first()
			db.session.delete(challenge)
			db.session.commit()
		except:
			return {"Status": "Failure. delete error"}, 400
		return {"Status": "Success!"}, 200

	return {"Status": "Failure. post error"}, 400

@app.route("/api/manage/challenges", methods=["GET"])
def get_challenges():
	results = [f"{c.points} {c.title} {c.instructions}" for c in Challenge.query.all()]
	return {"Status": "Success!", "Challenge": results}, 200


@app.route("/api/manage/solves", methods=["POST"])
def post_solves():
	pacific = pytz.timezone('America/Los_Angeles')

	if request.form["action"] == "create":
		try:
			timestamp = datetime.strptime(request.form["timestamp"], '%m-%d-%Y %H:%M')
			timestamp = pacific.localize(timestamp)
			solve = Solve(request.form["team"], request.form["challenge"], timestamp)
			db.session.add(solve)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "update":
		try:
			timestamp = datetime.strptime(request.form["timestamp"], '%m-%d-%Y %H:%M')
			timestamp = pacific.localize(timestamp)
			newTimestamp = datetime.strptime(request.form["newTimestamp"], '%m-%d-%Y %H:%M')
			newTimestamp = pacific.localize(newTimestamp)

			solve = Solve.query.filter_by(team=request.form["team"], challenge=request.form["challenge"], timestamp=timestamp).first()
			solve.team = request.form["newTeam"]
			solve.challenge = request.form["newChallenge"]
			solve.timestamp = newTimestamp
			db.session.add(solve)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success"}, 200

	elif request.form["action"] == "delete":
		try:
			timestamp = datetime.strptime(request.form["timestamp"], '%m-%d-%Y %H:%M')
			solve = Solve.query.filter_by(team=request.form["team"], challenge=request.form["challenge"], timestamp=timestamp).first()
			db.session.delete(solve)
			db.session.commit()
		except:
			return {"Status": "Failure. Delete error"}, 400
		return {"Status": "Success!"}, 200

@app.route("/api/manage/solves", methods=["GET"])
def get_solves():
	results = [f"{s.team} {s.challenge} {s.timestamp}" for s in Solve.query.all()]
	return {"Status": "Success!", "Solves": results}, 200



@app.route("/api/info", methods=["GET"])
def get_info():
	teamsresult = get_teams()
	playersresult = get_players()
	challengesresult = get_challenges()
	solvesresult = get_solves()
	return [teamsresult, playersresult, challengesresult, solvesresult]