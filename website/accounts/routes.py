from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from website import db
from website.accounts.forms import AccountForm
from website.models import Account

accounts = Blueprint("accounts", __name__)


@accounts.route("/accounts")
@login_required
def show_accounts():
    accs = Account.query.filter_by(user_id=current_user.id).all()
    return render_template("accounts.html", accounts=accs, user=current_user)


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
        )

        db.session.add(acc)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_account.html", title="New Account", form=form, legend="New Account"
    )


@accounts.route("/accounts/<int:acc_id>")
@login_required
def read_acc(acc_id):
    acc = Account.query.filter_by(user_id=current_user.id).get_or_404(acc_id)
    return render_template("acc.html", title=acc.name, post=acc)
