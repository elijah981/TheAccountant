from datetime import datetime, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from website import db
from website.accounts.forms import AccountForm
from website.models import Account

accounts = Blueprint("accounts", __name__)


@accounts.route("/accounts")
@login_required
def show_accounts():
    accs = Account.query.filter_by(user_id=current_user.id).all()
    return render_template("accounts.html", accounts=accs)


@accounts.route("/accounts/new", methods=["GET", "POST"])
@login_required
def new_account():
    form = AccountForm()
    if form.validate_on_submit():
        acc = Account(
            name=form.name.data,
            type=form.type.data,
            bank=form.bank.data,
            acc_num=form.acc_num.data,
            credit_card=form.credit_card.data,
            investment=form.investment.data,
            amount=form.amount.data,
            acc_holder=current_user,
            date=datetime.utcnow() + timedelta(hours=5, minutes=30),
        )

        db.session.add(acc)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("accounts.show_accounts"))
    return render_template(
        "create_account.html", title="New Account", form=form, legend="New Account"
    )


@accounts.route("/accounts/<int:acc_id>")
@login_required
def read_acc(acc_id):
    acc = Account.query.filter_by(user_id=current_user.id).get_or_404(acc_id)
    return render_template("acc.html", title=acc.name, post=acc)


@accounts.route("/accounts/<int:acc_id>/update", methods=["GET", "POST"])
@login_required
def update_account(acc_id):
    account = Account.query.filter_by(id=acc_id).first()
    if account.user_id != current_user.id:
        abort(403)
    form = AccountForm()
    if form.validate_on_submit():
        account.name = form.name.data
        account.type = form.type.data
        account.bank = form.bank.data
        account.acc_num = form.acc_num.data
        account.credit_card = form.credit_card.data
        account.investment = form.investment.data
        account.amount = form.amount.data
        account.date = datetime.utcnow() + timedelta(hours=5, minutes=30)
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("accounts.show_accounts"))
    elif request.method == "GET":
        form.name.data = account.name
        form.type.data = account.type
        form.bank.data = account.bank
        form.acc_num.data = account.acc_num
        form.credit_card.data = account.credit_card
        form.investment.data = account.investment
        form.amount.data = account.amount
        form.submit.label.text = "Update"

    return render_template(
        "create_account.html",
        title="Update Account",
        form=form,
        legend="Update Account",
    )


@accounts.route("/accounts/<int:acc_id>/delete", methods=["POST"])
@login_required
def delete_account(acc_id):
    account = Account.query.filter_by(id=acc_id).first()
    if account.user_id != current_user.id:
        abort(403)
    db.session.delete(account)
    db.session.commit()
    flash("Your account has been deleted!", "success")
    return redirect(url_for("accounts.show_accounts"))
