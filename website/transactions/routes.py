import ast

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from website import db
from website.models import Transaction

transactions = Blueprint("transactions", __name__)


@transactions.route("/transactions")
@login_required
def transactions_page():
    return render_template("transactions.html", title="About")


@transactions.route("/api/transactions", methods=["GET"])
@login_required
def get_transactions():
    """
    Api to get a list of all transactions
    """
    txns = Transaction.query.filter_by(user_id=current_user.id).all()

    data = []
    for txn in txns:
        data.append(
            {
                "id": txn.id,
                "date": txn.date,
                "from_name": txn.from_name,
                "to_name": txn.to_name,
                "txn_tag": txn.txn_tag,
                "description": txn.description,
                "amount": txn.amount,
            }
        )
    return jsonify({"data": data})


@transactions.route("/api/transactions/<int:txn_id>", methods=["GET"])
@login_required
def get_transaction(txn_id):
    """
    Api to get a list of all transactions
    """
    txn = (
        Transaction.query.filter_by(user_id=current_user.id)
        .filter_by(id=txn_id)
        .first()
    )

    data = {
        "id": txn.id,
        "date": txn.date,
        "from_name": txn.from_name,
        "to_name": txn.to_name,
        "txn_tag": txn.txn_tag,
        "description": txn.description,
        "amount": txn.amount,
    }

    return jsonify({"data": data})


@transactions.route("/api/transactions", methods=["POST"])
@login_required
def add_transaction():
    """
    Api to add transaction to db
    """
    byte_str = request.get_data()
    dict_str = byte_str.decode("UTF-8")
    data = ast.literal_eval(dict_str)

    txn = Transaction(
        txn_date=data.get("date"),
        from_name=data.get("from_name"),
        to_name=data.get("to_name"),
        txn_tag=data.get("data_tag"),
        description=data.get("description"),
        amount=data.get("amount"),
    )

    db.session.add(txn)
    db.session.commit()

    txn = (
        Transaction.query.filter_by(name=txn.date)
        .filter_by(name=txn.description)
        .filter_by(name=txn.amount)
        .first()
    )

    data = {
        "id": txn.id,
        "date": txn.date,
        "from_name": txn.from_name,
        "to_name": txn.to_name,
        "txn_tag": txn.txn_tag,
        "description": txn.description,
        "amount": txn.amount,
    }
    return jsonify(data)
