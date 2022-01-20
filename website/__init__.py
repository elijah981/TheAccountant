import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

with open("/etc/config.json") as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = config.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = config.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = config.get("EMAIL_PASS")
mail = Mail(app)

from website.users.routes import users
from website.posts.routes import posts
from website.main.routes import main
from website.accounts.routes import accounts
from website.budgets.routes import budgets
from website.transactions.routes import transactions


app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(accounts)
app.register_blueprint(budgets)
app.register_blueprint(transactions)
