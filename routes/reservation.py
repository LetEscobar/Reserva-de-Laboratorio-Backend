from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Reservation, Lab, User, ClassGroup
from dateutil.parser import parse

reservationBp = Blueprint('reservation', __name__)

@reservationBp.route('/', methods=['POST'])
def createReservation():
    data = request.json

    required_fields = ['labId', 'responsible', 'classGroupId', 'startTime']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400

    try:
        lab = Lab.query.get(data['labId'])
        if not lab:
            return jsonify({'error': 'Laboratório não encontrado'}), 404
        
        class_group = ClassGroup.query.get(data['classGroupId'])
        if not class_group:
            return jsonify({'error': 'Turma não encontrada'}), 404

        start_time = parse(data['startTime'])
        end_time = parse(data.get('endTime', data['startTime']))
        
        conflicting = Reservation.query.filter(
            Reservation.lab_id == data['labId'],
            Reservation.start_time < end_time,
            Reservation.end_time > start_time
        ).first()

        if conflicting:
            return jsonify({
                'error': 'Conflito de horário',
                'existing': {
                    'id': conflicting.id,
                    'start': conflicting.start_time.isoformat(),
                    'end': conflicting.end_time.isoformat()
                }
            }), 409

        reservation = Reservation(
            lab_id=data['labId'],
            responsible=data['responsible'],
            class_group_id=data['classGroupId'],
            students=','.join(map(str, data.get('students', []))),
            start_time=start_time,
            end_time=end_time,
            notes=data.get('notes', ''),
            repeat_weekly=data.get('repeatWeekly', False),
            repeat_until=parse(data['repeatUntil']) if data.get('repeatUntil') else None
        )
    
        db.session.add(reservation)
        db.session.commit()

        return jsonify({
            'message': 'Reserva criada com sucesso',
            'id': reservation.id,
            'lab': lab.name,
            'class_group': class_group.name
        }), 201

    except KeyError as e:
        return jsonify({'error': f'Campo obrigatório faltando: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Formato de data inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar reserva: {str(e)}'}), 500

@reservationBp.route('/', methods=['GET'])
def listReservations():
    lab_id = request.args.get('labId')
    if not lab_id:
        return jsonify({'error': 'Parâmetro labId é obrigatório'}), 400
        
    reservations = Reservation.query.filter_by(lab_id=lab_id).all()
    return jsonify([
        {
            'id': r.id,
            'start': r.start_time.isoformat(),
            'end': r.end_time.isoformat(),
            'responsible': r.responsible,
            'class_group': r.class_group.name,
            'students': r.students.split(',') if r.students else []
        }
        for r in reservations
    ])
