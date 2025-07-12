from flask import Blueprint, request, jsonify
from models import db, Lab, LabType

labBp = Blueprint('lab', __name__)

@labBp.route('/', methods=['GET', 'OPTIONS'])
def listLabs():
    if request.method == 'OPTIONS':
        return jsonify(), 200
    
    try:
        labs = Lab.query.filter_by(ativo=True).all()
        resultado = []
        for lab in labs:
            print(f"🔍 Lab: {lab.name}")
            tipo = lab.lab_type.name if lab.lab_type else "Sem tipo"
            print(f"📌 Tipo: {tipo}")
            reservas = lab.reservations or []
            resultado.append({
                'id': lab.id,
                'name': lab.name,
                'type': tipo,
                'reservations_count': len(reservas)
            })
        return jsonify(resultado)
    except Exception as e:
        print("❌ Erro ao listar labs:", e)
        return jsonify({'error': 'Erro ao buscar laboratórios'}), 500

@labBp.route('/', methods=['POST', 'OPTIONS'])
def create_lab():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json()
        print("Dados recebidos para criação de lab:", data)

        if not data or 'name' not in data or 'type' not in data:
            return jsonify({'error': 'Dados incompletos'}), 400
        
        lab_type = LabType.query.filter_by(name=data['type']).first()
        if not lab_type:
            lab_type = LabType(name=data['type'])
            db.session.add(lab_type)
            db.session.commit()

        new_lab = Lab(
            name=data['name'],
            lab_type_id=lab_type.id
        )
        db.session.add(new_lab)
        db.session.commit()

        return jsonify({
            'id': new_lab.id,
            'name': new_lab.name,
            'type': lab_type.name
        }), 201

    except Exception as e:
        db.session.rollback()
        print("❌ Erro ao criar laboratório:", e)
        return jsonify({'error': 'Erro interno ao criar laboratório'}), 500
