from flask import Blueprint, render_template
from flask_login import login_required

budgets = Blueprint("budgets", __name__)


@budgets.route("/budget")
@login_required
def budget():
    return render_template("budget.html", title="About")
