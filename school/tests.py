from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import Student, Teacher, Person, Schoolclass

class StudentTeacherModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_student_grade(self):
        s = Student(name='tom', email='tom@gmail.com', id=1, grade=10)
        print(s)
        
    def test_teacher_paygrade(self):
        t = Teacher(name='ann', email='ann@gmail.com', id=2, payGrade=99)
        print(t)

    def test_schoolclass(self):
        t1 = Teacher(name='ann', email='ann@gmail.com', id=2, payGrade=99)
        t2 = Teacher(name='mary', email='mary@gmail.com', id=3, payGrade=98)
        db.session.add_all([t1])
        db.session.commit()
        c1 = Schoolclass(subject='Algebra', classteacher=t1)
        c2 = Schoolclass(subject='Geometry', classteacher=t1)
        c3 = Schoolclass(subject='Trig')
        c4 = Schoolclass(subject='Geometry', classteacher=t2)
        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()
        print(c1)
        t1_clist = t1.schoolclasses
        print(t1_clist)
        print('before append', c3, 'anns classes are:', t1.schoolclasses.all())
        t1.schoolclasses.append(c3)
        db.session.commit()
        print('before append', c3, 'anns classes are:', t1.schoolclasses.all())
        print(Schoolclass.query.all())
        print('Mary classes:', t2.schoolclasses.all())
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
