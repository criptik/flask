from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
# ...


class Person(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def infoStr(self):
        return '%s, id=%d, email=%s' % (self.name, int(self.id), self.email)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.infoStr())

class Teacher(Person):
    __tablename__ = 'teacher'
    payGrade = db.Column(db.Integer)
    schoolclasses = db.relationship('Schoolclass', backref='classteacher', lazy='dynamic')
    # schoolclasses = db.relationship('Schoolclass', back_populates='classteacher', lazy='dynamic')

    def infoStr(self):
        return '%s, payGrade=%s' % (super().infoStr(), self.payGrade)

class Student(Person):
    __tablename__ = 'student'
    grade = db.Column(db.Integer)

    def infoStr(self):
        return '%s, grade=%s' % (super().infoStr(), self.grade)


# a Schoolclass has one teacher and many students.
# a teacher can have many Schoolclasses and so can a student
# so Teacher to SchoolClass is one-to-many
# but Student to SchoolClass is many-to-many

class Schoolclass(db.Model):
    __tablename__ = 'schoolclass'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(140))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    # classteacher = db.relationship('Teacher', back_populates='schoolclasses')
    
    def __repr__(self):
        tname = None if self.classteacher == None else self.classteacher.name
        return '<%s %s, teacher=%s>' % (self.__class__.__name__, self.subject, tname)
