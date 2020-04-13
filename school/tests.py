from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import Student, Teacher

class PersonModelCase(unittest.TestCase):
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
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
