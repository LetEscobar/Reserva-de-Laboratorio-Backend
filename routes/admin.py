from flask import Blueprint, request, jsonify
from models import db, User, Lab, LabType, Course, ClassGroup

adminBp = Blueprint('admin', __name__)


@adminBp.route('/users', methods=['POST'])
def createUser():
    data = request.json
    newUser = User(
        email=data['email'],
        password=data['password'],
        name=data['name'],
        isAdmin=False
    )
    db.session.add(newUser)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso'})

@adminBp.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
    user = User.query.get_or_404(id)
    data = request.json

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    db.session.commit()

    return jsonify({'message': 'Usuário atualizado com sucesso'})

@adminBp.route('/users/<int:id>/inativar', methods=['PATCH'])
def inativarUser(id):
    user = User.query.get_or_404(id)
    user.ativo = False
    db.session.commit()
    return jsonify({'message': 'Usuário inativado com sucesso'})


@adminBp.route('/labs', methods=['POST'])
def createLab():
    data = request.json
    typeName = data['type']
    labType = LabType.query.filter_by(name=typeName).first()
    if not labType:
        labType = LabType(name=typeName)
        db.session.add(labType)
        db.session.commit()

    lab = Lab(name=data['name'], labTypeId=labType.id)
    db.session.add(lab)
    db.session.commit()
    return jsonify({'message': 'Laboratório cadastrado com sucesso'})

@adminBp.route('/labs/<int:id>', methods=['PUT'])
def updateLab(id):
    lab = Lab.query.get_or_404(id)
    data = request.json

    lab.name = data.get('name', lab.name)

    if 'type' in data:
        typeName = data['type']
        labType = LabType.query.filter_by(name=typeName).first()
        if not labType:
            labType = LabType(name=typeName)
            db.session.add(labType)
            db.session.commit()
        lab.labTypeId = labType.id

    db.session.commit()
    return jsonify({'message': 'Laboratório atualizado com sucesso'})

@adminBp.route('/labs/<int:id>/inativar', methods=['PATCH'])
def inativarLab(id):
    lab = Lab.query.get_or_404(id)
    lab.ativo = False
    db.session.commit()
    return jsonify({'message': 'Laboratório inativado com sucesso'})


@adminBp.route('/classes', methods=['POST'])
def createClassGroup():
    data = request.json
    courseName = data['course']
    course = Course.query.filter_by(name=courseName).first()
    if not course:
        course = Course(name=courseName)
        db.session.add(course)
        db.session.commit()

    classGroup = ClassGroup(name=data['name'], courseId=course.id)
    db.session.add(classGroup)
    db.session.commit()
    return jsonify({'message': 'Turma cadastrada com sucesso'})

@adminBp.route('/classes/<int:id>', methods=['PUT'])
def updateClassGroup(id):
    classGroup = ClassGroup.query.get_or_404(id)
    data = request.json

    classGroup.name = data.get('name', classGroup.name)

    if 'course' in data:
        courseName = data['course']
        course = Course.query.filter_by(name=courseName).first()
        if not course:
            course = Course(name=courseName)
            db.session.add(course)
            db.session.commit()
        classGroup.courseId = course.id

    db.session.commit()
    return jsonify({'message': 'Turma atualizada com sucesso'})

@adminBp.route('/classes/<int:id>/inativar', methods=['PATCH'])
def inativarClassGroup(id):
    classGroup = ClassGroup.query.get_or_404(id)
    classGroup.ativo = False
    db.session.commit()
    return jsonify({'message': 'Turma inativada com sucesso'})


@adminBp.route('/courses/<int:id>', methods=['PUT'])
def updateCourse(id):
    course = Course.query.get_or_404(id)
    data = request.json

    course.name = data.get('name', course.name)
    db.session.commit()
    return jsonify({'message': 'Curso atualizado com sucesso'})

@adminBp.route('/courses/<int:id>/inativar', methods=['PATCH'])
def inativarCourse(id):
    course = Course.query.get_or_404(id)
    course.ativo = False
    db.session.commit()
    return jsonify({'message': 'Curso inativado com sucesso'})
