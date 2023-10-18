from __future__ import annotations

import bcrypt

from app import db

from flask_login import UserMixin
from typing import Union

from datetime import datetime
import pytz

class Team(UserMixin, db.Model):

	__tablename__ = "teams"

	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(256), unique=True , nullable=False)
	password = db.Column(db.String(256), unique=False, nullable=False)

	def __init__(self, name, password, userType=1):

		# Name and password cannot be blank.
		assert name != None and password != None

		# Name must be unique.
		assert Team.query.filter_by(name=name).first() == None

		self.name = name
		self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(4))

	def get_team(id: int) -> Union[Team, None]:
		"""
		Get a team using their ID. 
		"""

		return Team.query.filter_by(id=id).first()

	def login(name: str, password: str) -> Union[User, None]:
		"""
		Log into an account.
		"""

		try:
			assert (team:=Team.query.filter_by(name=name).first()) != None
			assert bcrypt.checkpw(password.encode(), team.password)
			return team
		except:
			return None

class Player(db.Model):

	__tablename__ = "players"

	id = db.Column(db.Integer, primary_key=True)
	team = db.Column(db.Integer, db.ForeignKey(Team.id), unique=False, nullable=False)
	name = db.Column(db.String(256), unique=False, nullable=False)

	def __init__(self, team, name):

		# Team and name cannot be blank.
		assert team != None and name != None

		self.team = team
		self.name = name

class Challenge(db.Model):

	__tablename__ = "challenges"

	id = db.Column(db.Integer, primary_key=True)
	points = db.Column(db.Integer, unique=False, nullable=False) #points not unique since multiple teams can have same amount of points, nullable true becasue players can have zero points?
	title = db.Column(db.String(256), unique=False, nullable=False) #challenge names should be different? challenges should all have titles.and
	instructions = db.Column(db.String(256), unique=False, nullable=False)#challenge instruct. should be differnet, challenge needs to have instructions

	def __init__(self, points, title, instructions):

		assert points != None and title != None and instructions != None

		self.points = points
		self.title = title
		self.instructions = instructions

class Solve(db.Model):
	__tablename__ = "solves"

	id = db.Column(db.Integer, primary_key=True)

	pacific = pytz.timezone('America/Los_Angeles')

	team = db.Column(db.Integer, db.ForeignKey(Team.id), unique=False, nullable=False)
	challenge = db.Column(db.String(256), db.ForeignKey(Challenge.id), unique=False, nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

	def __init__(self, team, challenge, timestamp=None):
		assert team != None and challenge != None 
	
		self.team = team
		self.challenge = challenge
		self.timestamp = timestamp if timestamp else pacific.localize(datetime.utcnow())
