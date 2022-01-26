from datetime import datetime, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from website import db
from website.budgets.forms import BudgetForm
from website.models import Budget

budgets = Blueprint("budgets", __name__)


@budgets.route("/budgets")
@login_required
def show_budgets():
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    return render_template("budgets.html", budgets=budgets)


@budgets.route("/budgets/new", methods=["GET", "POST"])
@login_required
def new_budget():
    form = BudgetForm()
    if form.validate_on_submit():
        budget = Budget(
            name=form.name.data,
            initial=form.initial.data,
            present=form.present.data,
            tenure=form.tenure.data,
            acc_holder=current_user,
            date=datetime.utcnow() + timedelta(hours=5, minutes=30),
        )

        db.session.add(budget)
        db.session.commit()
        flash("Your budget has been created!", "success")
        return redirect(url_for("budgets.show_budgets"))
    return render_template(
        "create_budget.html", title="New Budget", form=form, legend="New Budget"
    )


@budgets.route("/budgets/<int:budget_id>/update", methods=["GET", "POST"])
@login_required
def update_budget(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget.user_id != current_user.id:
        abort(403)
    form = BudgetForm()
    if form.validate_on_submit():
        budget.name = form.name.data
        budget.initial = form.initial.data
        budget.present = form.present.data
        budget.tenure = form.tenure.data
        budget.date = datetime.utcnow() + timedelta(hours=5, minutes=30)
        db.session.commit()
        flash("Your budget has been updated!", "success")
        return redirect(url_for("budgets.show_budgets"))
    elif request.method == "GET":
        form.name.data = budget.name
        form.initial.data = budget.initial
        form.present.data = budget.present
        form.tenure.data = budget.tenure
        form.submit.label.text = "Update"

    return render_template(
        "create_budget.html",
        title="Update budget",
        form=form,
        legend="Update budget",
    )


@budgets.route("/budgets/<int:budget_id>/delete", methods=["POST"])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget.user_id != current_user.id:
        abort(403)
    db.session.delete(budget)
    db.session.commit()
    flash("Your budget has been deleted!", "success")
    return redirect(url_for("budgets.show_budgets"))
