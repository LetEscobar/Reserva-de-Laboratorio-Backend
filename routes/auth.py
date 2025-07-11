from flask import Blueprint, request, jsonify
from models import db, User

authBp = Blueprint('auth', __name__)

@authBp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json(force=True, silent=True)

        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Campos obrigatórios não enviados'}), 400

        print("Dados recebidos:", data)

        user = User.query.filter_by(email=data['email'], password=data['password']).first()

        if user:
            return jsonify({'message': 'Login realizado com sucesso', 'isAdmin': user.is_admin}), 200

        return jsonify({'message': 'Credenciais inválidas'}), 401

    except Exception as e:
        print("Erro interno no login:", str(e))
        return jsonify({'error': 'Erro interno no servidor'}), 500


@authBp.route('/register_public', methods=['POST'])
def register_public():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    senha = data.get('senha')

    if not name or not email or not senha:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'E-mail já cadastrado'}), 400

    new_user = User(name=name, email=email, senha=senha, is_admin=False, status='ativo')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'id': new_user.id, 'name': new_user.name}), 201
