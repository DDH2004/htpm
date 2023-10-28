import os
import sys

from flask import *
from flask_sqlalchemy import *

# Instantiate the application and define settings.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.urandom(32)

# Load the database.
db = SQLAlchemy(app)
from model import *

# Make the database.
with app.app_context():
	db.create_all()

	# If the admin team doesn't exist, auto-make a default one.
	if Team.query.filter_by(username="admin").first() == None:
		account = Team("admin", "12345678")
		db.session.add(account)
		db.session.commit()

from security import *
from route import *
from api import *
