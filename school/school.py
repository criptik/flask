from app import app, db
from app.models import Person, Teacher, Student, Schoolclass

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Person': Person, 'Teacher': Teacher, 'Student' : Student, 'Schoolclass' : Schoolclass}
