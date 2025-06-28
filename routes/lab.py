from flask import Blueprint, jsonify
from models import Lab

labBp = Blueprint('lab', __name__)

@labBp.route('/', methods=['GET'])
def listLabs():
    labs = Lab.query.filter_by(ativo=True).all()
    return jsonify([
        {
            'id': lab.id,
            'name': lab.name,
            'type': lab.labType.name
        } for lab in labs
    ])
