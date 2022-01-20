import enum
from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from website import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)  # to be removed
    accounts = db.relationship("Account", backref="acc_holder", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    txn_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    txn_from = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    from_name = db.Column(db.String(100), nullable=True)
    txn_to = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    to_name = db.Column(db.String(100), nullable=True)
    txn_tag = db.Column(db.Integer, db.ForeignKey("budget.id"), nullable=False)
    tag_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Transaction('{self.title}', '{self.amount}')"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    bank = db.Column(db.String(100), nullable=False)
    acc_num = db.Column(db.String(100), nullable=True)
    credit_card = db.Column(db.Boolean, nullable=False)
    investment = db.Column(db.Boolean, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Account('{self.name}')"


class frequency(enum.Enum):
    monthly = 1
    yearly = 2
    nolimit = 3


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    initial = db.Column(db.Float, nullable=False)
    present = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tenure = db.Column(db.Enum(frequency), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Budget('{self.title}', '{self.amount}')"
