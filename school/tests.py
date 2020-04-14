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
        t1 = Teacher(name='jane', email='jane@gmail.com', id=2, payGrade=99)
        t2 = Teacher(name='mary', email='mary@gmail.com', id=3, payGrade=98)
        db.session.add_all([t1])
        db.session.commit()
        c1 = Schoolclass(subject='Algebra', classteacher=t1)
        c2 = Schoolclass(subject='Geometry', classteacher=t1)
        c3 = Schoolclass(subject='Trig')
        c4 = Schoolclass(subject='Geometry', classteacher=t2)
        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()
        # t1 before append
        self.assertEqual(t1.schoolclasses.all(), [c1, c2])
        self.assertEqual(c3.classteacher, None)
        # do append
        t1.schoolclasses.append(c3)
        db.session.commit()
        # test after append
        self.assertEqual(t1.schoolclasses.all(), [c1, c2, c3])
        self.assertEqual(c3.classteacher, t1)

        self.assertEqual(Schoolclass.query.all(), [c1, c2, c3, c4])
        # check Mary classes
        self.assertEqual(t2.schoolclasses.all(), [c4])

        s1 = Student(name='john', email='john@gmail.com', id=11)
        s2 = Student(name='gina', email='gina@gmail.com', id=12)
        s3 = Student(name='pat', email='pat@gmail.com', id=13)

        s1.studclasses.append(c1)
        s1.studclasses.append(c3)
        s2.studclasses.append(c1)
        s2.studclasses.append(c3)
        s2.studclasses.append(c4)
        s3.studclasses.append(c4)
        db.session.commit()
        print()
        n = 1
        for s in [s1, s2, s3]:
            print('s%d, (%s) students are %s' % (n, s, s.studclasses.all()))
            n = n + 1

        c2.students.append(s1)
        db.session.commit()
        print('-----------------')
        n = 1
        for c in [c1, c2, c3, c4]:
            print('c%d, (%s) students are %s' % (n, c, c.students))
            n = n + 1
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
