from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Teacher(db.Model):
    __tablename__="teachers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.column(db.String, nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    @classmethod
    def authenticate(cls, username, password):
        """Check username and password with bcrypt against db
        returns user if username and password match, False if not"""
        teacher = Teacher.query.filter_by(username=username).first()
        if teacher and bcrypt.check_password_hash(teacher.password, password):
            return teacher
        else:
            return False

class Student(db.Model):
    __tablename__="students"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))

    @classmethod
    def authenticate(cls, username, password):
        """Check username and password with bcrypt against db
        returns user if username and password match, False if not"""
        student = Student.query.filter_by(username=username).first()
        if student and bcrypt.check_password_hash(student.password, password):
            return student
        else:
            return False
        
class Assignment(db.Model):
    __tablename__="assignments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))

    student = db.relationship("Student", secondary="students_assignments", backref="assignment")
    
class StudentAssignment(db.Model):
    __tablename__="students_assignments"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"))
    completed = db.Column(db.Boolean, default=False)
    grade = db.Column(db.Integer, default=0)
    