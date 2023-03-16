from flask import Blueprint
from app import db, models

login_bp = Blueprint("login_bp", __name__)


@login_bp.route('/login')
def login():
    # db.insert()
    return "OK"
