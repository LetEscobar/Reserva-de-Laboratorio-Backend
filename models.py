from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    ativo = db.Column(db.Boolean, default=True)
    
class LabType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    labs = db.relationship('Lab', backref='labType', lazy=True)

class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    labTypeId = db.Column(db.Integer, db.ForeignKey('lab_type.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=True)

class ClassGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    courseId = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    course = db.relationship('Course', backref='classes')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    labId = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)
    responsible = db.Column(db.String(100), nullable=False)
    classGroupId = db.Column(db.Integer, db.ForeignKey('class_group.id'), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    repeatWeekly = db.Column(db.Boolean, default=False)
    repeatUntil = db.Column(db.DateTime)

    lab = db.relationship('Lab', backref='reservations')
    classGroup = db.relationship('ClassGroup', backref='reservations')
