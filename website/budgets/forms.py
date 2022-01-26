from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class BudgetForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    initial = FloatField("Budget", validators=[DataRequired()])
    present = FloatField("Used", validators=[DataRequired()])
    tenure = SelectField(
        "Frequency",
        choices=[("monthly", "monthly"), ("yearly", "yearly"), ("nolimit", "no limit")],
    )
    submit = SubmitField("Create")
