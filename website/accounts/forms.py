from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, StringField, SubmitField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    type = StringField("Type", validators=[DataRequired()])
    bank = StringField("Bank", validators=[DataRequired()])
    acc_num = StringField("Account No.", validators=[DataRequired()])
    credit_card = BooleanField("Is this a credit card?")
    investment = BooleanField("Is this a investment?")
    amount = FloatField("Amount", validators=[DataRequired()])
    submit = SubmitField("Create")
