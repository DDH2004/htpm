from app import *

from flask_login import current_user, login_required

@app.route("/api/manage/teams", methods=["POST"])
@login_required
def post_teams():

	if current_user.username != "admin":
		return redirect(url_for("login"))

	if request.form["action"] == "create":
		try:
			team = Team(request.form["name"], request.form["password"])
			db.session.add(team)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "update":
		try:
			team = Team.query.filter_by(name=request.form["name"]).first()
			team.name = request.form["newName"]
			team.password = request.form["newPassword"]
			db.session.add(team)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "delete":
		try:
			team = Team.query.filter_by(name=request.form["name"]).first()
			db.session.delete(team)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	return {"Status": "Failure."}, 400

@app.route("/api/manage/teams", methods=["GET"])
@login_required
def get_teams():

	if current_user.username != "admin":
		return redirect(url_for("login"))

	results = [(t.id, t.name, t.password) for t in Team.query.all()]
	return {"Status": "Success!", "Teams": results}, 200

@app.route("/api/manage/players", methods=["POST"])
@login_required
def post_players():

	if current_user.username != "admin":
		return redirect(url_for("login"))

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
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "delete":
		try:
			player = Player.query.filter_by(team=request.form["team"], name=request.form["name"]).first()
			db.session.delete(player)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	return {"Status": "Failure."}, 400

@app.route("/api/manage/players", methods=["GET"])
@login_required
def get_players():

	if current_user.username != "admin":
		return redirect(url_for("login"))

	results = [(p.team,p.name) for p in Player.query.all()]
	return {"Status": "Success!", "Teams": results}, 200

@app.route("/api/manage/challenges", methods=["POST"])
@login_required
def post_challenges():

	if current_user.username != "admin":
		return redirect(url_for("login"))

	if request.form["action"] == "create":
		try:
			challenge = Challenge(request.form["title"])
			db.session.add(challenge)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200
		
	elif request.form["action"] == "update":
		try:
			challenge = Challenge.query.filter_by(title=request.form["title"]).first()
			challenge.title = request.form["newTitle"]
			db.session.add(challenge)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200
	
	elif request.form["action"] == "delete":
		try:
			challenge = Challenge.query.filter_by(title=request.form["title"]).first()
			db.session.delete(challenge)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	return {"Status": "Failure."}, 400

@app.route("/api/manage/challenges", methods=["GET"])
@login_required
def get_challenges():

	if current_user.username != "admin":
		return redirect(url_for("login"))

	results = [c.title for c in Challenge.query.all()]
	return {"Status": "Success!", "Challenges": results}, 200

@app.route("/api/manage/solves", methods=["POST"])
@login_required
def post_solves():

	if current_user.username != "admin":
		return redirect(url_for("login"))

	if request.form["action"] == "create":
		try:
			timestamp = request.form["timestamp"]
			solve = Solve(request.form["team"], request.form["challenge"], timestamp)
			db.session.add(solve)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "update":
		try:
			solve = Solve.query.filter_by(team=request.form["team"], challenge=request.form["challenge"]).first()
			solve.team = request.form["newTeam"]
			solve.challenge = request.form["newChallenge"]
			solve.timestamp = request.form["newTimestamp"]
			db.session.add(solve)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

	elif request.form["action"] == "delete":
		try:
			timestamp = datetime.strptime(request.form["timestamp"], '%m-%d-%Y %H:%M')
			solve = Solve.query.filter_by(team=request.form["team"], challenge=request.form["challenge"]).first()
			db.session.delete(solve)
			db.session.commit()
		except Exception as e:
			print(e)
			return {"Status": "Failure."}, 400
		return {"Status": "Success!"}, 200

@app.route("/api/manage/solves", methods=["GET"])
@login_required
def get_solves():

	if current_user.username != "admin":
		return redirect(url_for("login"))

	results = [(s.team,s.challenge,s.timestamp) for s in Solve.query.all()]
	return {"Status": "Success!", "Solves": results}, 200

