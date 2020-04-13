from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
# ...


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def infoStr(self):
        return '%s, id=%d, email=%s' % (self.name, int(self.id), self.email)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.infoStr())

class Teacher(Person):
    payGrade = db.Column(db.Integer)

    def infoStr(self):
        return '%s, payGrade=%s' % (super().infoStr(), self.payGrade)

class Student(Person):
    grade = db.Column(db.Integer)

    def infoStr(self):
        return '%s, grade=%s' % (super().infoStr(), self.grade)

