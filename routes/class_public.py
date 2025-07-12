from flask import Blueprint, request, jsonify
from models import db, User, ClassGroup

classPublicBp = Blueprint('classPublic', __name__)

@classPublicBp.route('/classes', methods=['GET'])
def listClasses():
    classes = ClassGroup.query.filter_by(ativo=True).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in classes])


@classPublicBp.route('/classes', methods=['POST'])
def create_class():
    data = request.json
    name = data.get('name')
    course = data.get('course')

    if not name or not course:
        return jsonify({'error': 'Nome e curso são obrigatórios'}), 400

    new_class = ClassGroup(name=name, course=course)
    db.session.add(new_class)
    db.session.commit()

    return jsonify({'id': new_class.id, 'name': new_class.name}), 201
