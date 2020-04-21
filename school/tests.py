from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import Student, Teacher, Person, Schoolclass
import sys

class table1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    col1 = db.Column(db.Integer)
    col3 = db.Column(db.Integer)
    # other columns
    def __repr__(self):
        return '(%d, %d)' % (self.col1, self.col3)

class table2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    col2 = db.Column(db.Integer)
    col3 = db.Column(db.Integer)
    # other columns
    def __repr__(self):
        return '(%d, %d)' % (self.col2, self.col3)

class StudentTeacherModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def test_student_grade(self):
    #     s = Student(name='tom', email='tom@gmail.com', grade=10)
    #     db.session.add(s)
    #     db.session.commit()
    #     print(s)
        
    # def test_teacher_paygrade(self):
    #     t = Teacher(name='ann', email='ann@gmail.com', payGrade=99)
    #     db.session.add(t)
    #     db.session.commit()
    #     print(t)


    def not_test_tablejoin(self):
        t1s = []
        t2s = []
        for n in range(1,6):
            t1s.append(table1(col1 = n, col3 = 2*n % 5))
        db.session.add_all(t1s)
        db.session.commit()
        for n in range(1,6):
            t2s.append(table2(col2 = 2*n, col3 = 2*n % 10))
        db.session.add_all(t2s)
        db.session.commit()
        print()
        print('t1s', table1.query.all())
        print('t2s', table2.query.all())
        
        q1 = db.session.query(table1.col1, table2.col2).filter(table1.col3 == table2.col3)
        print('q1 is', q1.statement)
        print('q1 all is ', q1.all())

        q2 = db.session.query(table1.col1, table2.col2).join(table2, table1.col3 == table2.col3)
        print('q2 is', q2.statement)
        print('q2 all is ', q2.all())
        return

    def showClassStuds(self, n, c):
        print('Class c%d, (%s) students are: ' % (n, c), end='')
        for s in c.students:
            print(s.name, end=' ')
        print()
        
    
    def test_schoolclass(self):
        numTeachers = 4
        teachers = []
        for n in range(numTeachers):
            tname = 't%d' % (n)
            temail = '%s@gmail.com' % (tname)
            teachers.append(Teacher(name=tname, email=temail, payGrade=90+n))
        db.session.add_all(teachers)
        db.session.commit()

        numStuds = 25
        studs = []
        for n in range(numStuds):
            sname = 's%d' % (n)
            semail = '%s@gmail.com' % (sname)
            studs.append(Student(name=sname, email=semail))
        db.session.add_all(studs)
        db.session.commit()

        numClasses = 5
        classes = []
        subjects = ['Algebra', 'Geometry', 'Trig', 'Calculus']
        for n in range(numClasses):
            # add last class with no teacher
            if n < numClasses-1:
                ct = teachers[n%2]
            else:
                ct = None
            classes.append(Schoolclass(subject=subjects[n%4], classteacher=ct))
        db.session.add_all(classes)
        db.session.commit()

        print()
        # print(teachers[0].getStudents())
        
        # t[0] before append
        self.assertEqual(teachers[0].schoolclasses.all(), [classes[0], classes[2]])
        self.assertEqual(classes[4].classteacher, None)
        # do append
        teachers[0].schoolclasses.append(classes[-1])
        db.session.commit()
        # test after append
        self.assertEqual(teachers[0].schoolclasses.all(), [classes[0], classes[2], classes[4]])
        self.assertEqual(classes[4].classteacher, teachers[0])

        self.assertEqual(Schoolclass.query.all(), classes)
        # check teacher[1] classes
        self.assertEqual(teachers[1].schoolclasses.all(), [classes[1], classes[3]])

        # assign students to classes
        n = 0
        for s in studs:
            if n >= numStuds-2:
                continue
            s.studclasses.append(classes[n % (numClasses-1)])
            print('s%d in c%d' % (n, n  % (numClasses-1)))
            if n == 1:
                s.studclasses.append(classes[2])
                s.studclasses.append(classes[3])
                print('s1 in c2, c3')
            n = n + 1
        db.session.commit()

        print('Before append, ', end='')
        self.showClassStuds(1, classes[1])
        
        # appending s0 to c1
        classes[1].students.append(studs[0])
        db.session.commit()
        print()
        print('After Append -----------------')
        n = 0
        for c in classes:
            self.showClassStuds(n, classes[n])
            n = n + 1

        print('+++')

        for t in teachers:
            print('Student List for %s:' % (t.name), end=' ')
            for s in t.getStudents():
                print(s.name, end=' ')
            print()

        n = 0
        for s in studs:
            print('Student %s: classes are %s' % (s.name, s.studclasses.all()))
            n = n + 1

        if False:
            # record a grade
            # get first class and first student in that class
            clazz = teachers[0].getClasses()[0]
            stud = clazz.students[0]
            teachers[0].recordClassGrade(clazz, stud, 98)
            db.session.commit()
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
