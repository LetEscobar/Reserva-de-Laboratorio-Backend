from flask import Blueprint, request, jsonify
from models import db, User

authBp = Blueprint('auth', __name__)

@authBp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify({'message': 'Login realizado com sucesso', 'isAdmin': user.isAdmin})
    return jsonify({'message': 'Credenciais inválidas'}), 401
