from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, name='isAdmin')
    ativo = db.Column(db.Boolean, default=True)


class LabType(db.Model):
    __tablename__ = 'labtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    labs = db.relationship('Lab', back_populates='lab_type', lazy=True)


class Lab(db.Model):
    __tablename__ = 'labs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lab_type_id = db.Column(db.Integer, db.ForeignKey('labtype.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    lab_type = db.relationship('LabType', back_populates='labs')
    reservations = db.relationship('Reservation', back_populates='lab', lazy=True)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    class_groups = db.relationship('ClassGroup', back_populates='course', lazy=True)


class ClassGroup(db.Model):
    __tablename__ = 'classgroup'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), name='courseId', nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    course = db.relationship('Course', back_populates='class_groups')
    reservations = db.relationship('Reservation', back_populates='class_group', lazy=True)


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'), nullable=False)
    responsible = db.Column(db.String(100), nullable=False)
    class_group_id = db.Column(db.Integer, db.ForeignKey('classgroup.id'), name='classGroupId', nullable=False)
    start_time = db.Column(db.DateTime, name='startTime', nullable=False)
    end_time = db.Column(db.DateTime, name='endTime', nullable=False)
    notes = db.Column(db.Text)
    repeat_weekly = db.Column(db.Boolean, name='repeatWeekly', default=False)
    repeat_until = db.Column(db.DateTime, name='repeatUntil')

    lab = db.relationship('Lab', back_populates='reservations')
    class_group = db.relationship('ClassGroup', back_populates='reservations')
