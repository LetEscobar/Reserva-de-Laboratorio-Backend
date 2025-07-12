from flask import Blueprint, jsonify
from models import User

userPublicBp = Blueprint('userPublic', __name__)

@userPublicBp.route('/users', methods=['GET'])
def listUsers():
    users = User.query.filter_by(ativo=True).all()
    return jsonify([{'id': u.id, 'name': u.name} for u in users])

@userPublicBp.route('/users', methods=['GET'])
def get_users():
    users = User.query.filter_by(is_admin=False).all()
    return jsonify([{'id': u.id, 'name': u.name} for u in users])
