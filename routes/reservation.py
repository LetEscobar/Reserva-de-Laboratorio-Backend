from flask import Blueprint, request, jsonify
from models import db, Reservation
from datetime import datetime, timedelta

reservationBp = Blueprint('reservation', __name__)

@reservationBp.route('/', methods=['POST'])
def createReservation():
    data = request.json
    startTime = datetime.fromisoformat(data['startTime'])
    endTime = datetime.fromisoformat(data['endTime'])
    repeatWeekly = data.get('repeatWeekly', False)
    repeatUntil = datetime.fromisoformat(data['repeatUntil']) if data.get('repeatUntil') else None

    reservations = []

    while True:
        newReservation = Reservation(
            labId=data['labId'],
            responsible=data['responsible'],
            classGroupId=data['classGroupId'],
            startTime=startTime,
            endTime=endTime,
            notes=data.get('notes', ''),
            repeatWeekly=repeatWeekly,
            repeatUntil=repeatUntil
        )
        db.session.add(newReservation)
        reservations.append(newReservation)

        if not repeatWeekly or not repeatUntil:
            break

        startTime += timedelta(weeks=1)
        endTime += timedelta(weeks=1)
        if startTime > repeatUntil:
            break

    db.session.commit()
    return jsonify({'message': f'{len(reservations)} reserva(s) criada(s) com sucesso'})

@reservationBp.route('/', methods=['GET'])
def listReservations():
    labId = request.args.get('labId')
    reservations = Reservation.query.filter_by(labId=labId).all()
    return jsonify([
        {
            'id': r.id,
            'responsible': r.responsible,
            'startTime': r.startTime.isoformat(),
            'endTime': r.endTime.isoformat(),
            'classGroup': r.classGroup.name,
            'notes': r.notes
        } for r in reservations
    ])
