from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
import sys

# for the many-to-many student-class relationship
studentclassinfo = db.Table('studentclassinfo',
                            db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                            db.Column('class_id', db.Integer, db.ForeignKey('schoolclass.id')),
                            db.Column('class_grade', db.Integer),
                            db.PrimaryKeyConstraint('student_id', 'class_id') )


class Person(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def infoStr(self):
        return '%s, id=%d' % (self.name, int(self.id))

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.infoStr())

class Teacher(Person):
    __tablename__ = 'teacher'
    payGrade = db.Column(db.Integer)
    schoolclasses = db.relationship('Schoolclass', backref='classteacher', lazy='dynamic')
    # schoolclasses = db.relationship('Schoolclass', back_populates='classteacher', lazy='dynamic')

    def infoStr(self):
        return '%s, payGrade=%s' % (super().infoStr(), self.payGrade)

    # get all classes that this teacher teaches
    def getClasses(self):
        return self.schoolclasses.all()

    # get all students who take a class from this teacher
    def getStudents(self):
        if False:
            # simple one using a set and no SQL calls
            studs = set({})
            for c in self.getClasses():
                for s in c.students:
                    studs.add(s)
            return studs
        elif False:
            # try to use SQL join and filter by test against myclassids
            myclassids = []
            for c in self.getClasses():
                myclassids.append(c.id)
            # print('myclassids:', myclassids)
            q = (Student.query.join(studentclassinfo, (studentclassinfo.c.student_id == Student.id))
                 .filter(studentclassinfo.c.class_id.in_(myclassids))
                 .order_by(Student.name))
            # print('SQL is', q)
            return q.all()
        else:
            # try without any data structures that are outside the db
            q = (Student.query.join(studentclassinfo, (studentclassinfo.c.student_id == Student.id))
                 .join(Schoolclass, (Schoolclass.id == studentclassinfo.c.class_id))
                 .filter(Schoolclass.teacher_id == self.id)
                 .order_by(Student.name))
            # print('SQL is ', q)
            return q.all()

    # def recordClassGrade(self, clazz, stud, classGrade):
    #     # get record from studentclassinfo table
    #     info = studentclassinfo.query().filter(studentclassinfo.c.class_id == clazz.id,
    #                                            studentclassinfo.c.student_id == stud.id).all()
    #     print('before classGrade:', info.__dict__)
    #     if info == []:
    #         print('Error no such class-student combination registered')
    #         return

    #     info.class_grade = classGrade
    #     print('afterbefore classGrade:', info.__dict__)
        
        
class Student(Person):
    __tablename__ = 'student'
    grade = db.Column(db.Integer)
    studclasses = db.relationship(
        'Schoolclass', secondary=studentclassinfo,
        backref = 'students',
        lazy='dynamic')

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
    
    def __repr__(self):
        tname = None if self.classteacher == None else self.classteacher.name
        return '<%s %s, teacher=%s, id=%d>' % (self.__class__.__name__, self.subject, tname, self.id)

    def get_teacher_id(self):
        return self.teacher_id

    def student_ids(self):
        ids = []
        for s in self.students:
            ids.append(s.id)
        return ids
        
    
