from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
import sys

# one student can point to many studentclassinfo records
class StudentClassInfo(db.Model):
    __table_name__ = 'studentclassinfo'
    __table_args__ = (
        db.PrimaryKeyConstraint('student_id', 'class_id'),
    )
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('schoolclass.id'))
    class_grade = db.Column(db.Integer)

    def __repr__(self):
        return '<cid=%d, sid=%d, gr=%s>' % (self.class_id, self.student_id, self.class_grade)
    
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
    classesTaught = db.relationship('Schoolclass', backref='classteacher', lazy='dynamic')

    def infoStr(self):
        return '%s, payGrade=%s' % (super().infoStr(), self.payGrade)

    # get all classes that this teacher teaches
    def getClasses(self):
        return self.classesTaught.all()

    # get all students who take a class from this teacher
    def getStudents(self):
        if False:
            # simple one using a set and no SQL calls
            studs = set({})
            for c in self.getClasses():
                for s in c.students:
                    studs.add(s)
            return studs
        else:
            # try without any data structures that are outside the db
            q = (Student.query.join(StudentClassInfo, (StudentClassInfo.student_id == Student.id))
                 .join(Schoolclass, (Schoolclass.id == StudentClassInfo.class_id))
                 .filter(Schoolclass.teacher_id == self.id)
                 .order_by(Student.name))
            # print('SQL is ', q)
            return q.all()

    def recordClassGrade(self, clazz, stud, classGrade):
        # get record from studentclassinfo table
        debug = False
        if debug:
            print('recordClassGrade ', self, clazz, stud, classGrade)
        infoArray = StudentClassInfo.query.filter(StudentClassInfo.class_id == clazz.id,
                                                  StudentClassInfo.student_id == stud.id).all()
        if len(infoArray) == 0:
            print('Error no such class-student combination registered')
            return

        info = infoArray[0]
        if debug:
            print('before classGrade:', info)
        info.class_grade = classGrade
        if debug:
            print('after classGrade:', info)
        
        
class Student(Person):
    __tablename__ = 'student'
    grade = db.Column(db.Integer)
    studClassInfos = db.relationship('StudentClassInfo', backref = 'student',  lazy='dynamic')

    def infoStr(self):
        return '%s, grade=%s' % (super().infoStr(), self.grade)

    def getClasses(self):
        if False:
            # non join version
            classes = []
            for info in self.studClassInfos.all():
                classes.append(Schoolclass.query.get(info.class_id))
            return classes
        else:
            # joiny version
            result = (Schoolclass.query
                      .join(StudentClassInfo)  
                      .filter(StudentClassInfo.student_id == self.id)
                      .order_by(Schoolclass.id)
                      .all())
            return result
            
    def registerForClass(self, clazz):
        info = StudentClassInfo(class_id = clazz.id, class_grade = None)
        self.studClassInfos.append(info)
        db.session.add(info)
        db.session.commit()

    def getClassGrade(self, clazz):
        for info in self.studClassInfos.all():
            if info.class_id == clazz.id:
                return info.class_grade
        return None
    
        
# a Schoolclass has one teacher and many students.
# a teacher can have many Schoolclasses and so can a student
# so Teacher to SchoolClass is one-to-many
# but a SchoolClassInfo record (includes grade_mark) only has one student

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

    # get all students in this class
    def getStudents(self):
        result = (Student.query
                  .join(StudentClassInfo)  #, (StudentClassInfo.class_id == self.id))
                  .filter(StudentClassInfo.class_id == self.id)
                  .order_by(Student.name)
                  .all())
        if False:
            print()
            print('my class id is ', self.id)
            print('all students = ', Student.query.all())
            print('all infos = ', StudentClassInfo.query.all())
            print('all join-filter = ', result)
        return result
            
    def getStudentIds(self):
        ids = []
        for s in self.getStudents():
            ids.append(s.id)
        return ids
        
    
