from flask import Blueprint, jsonify
from models import ClassGroup

classPublicBp = Blueprint('classPublic', __name__)

@classPublicBp.route('/classes', methods=['GET'])
def listActiveClasses():
    classes = ClassGroup.query.filter_by(ativo=True).all()
    return jsonify([
        {
            'id': turma.id,
            'name': turma.name,
            'course': turma.course.name
        } for turma in classes
    ])
