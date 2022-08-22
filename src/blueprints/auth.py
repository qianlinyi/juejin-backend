from flask import Blueprint, jsonify, request
from src.extensions import db
from src.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        if username == user.username and user.validate_password(password):
            response = {'status': 'success'}
            return jsonify(response)
        else:
            response = {'status': 'failed', 'description': '密码错误'}
            return jsonify(response)
    else:
        response = {'status': 'failed', 'description': '账户不存在'}
        return jsonify(response)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('confirm-password')
    if password != password2:
        response = {'status': 'failed', 'description': '密码不匹配'}
        return jsonify(response)
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    response = {'status': 'success'}
    return jsonify(response)
