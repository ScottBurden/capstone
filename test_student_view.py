# run with python3 -m unittest test_message_model.py

from app import app
import os
from unittest import TestCase
from models import db, Teacher, Student, StudentAssignment, Assignment

os.environ['DATABASE_URL'] = "postgresql:///capstone_school"

app.config['WTF_CSRF_ENABLED'] = False
app.config["DEBUG_TB_HOSTS"]=["dont-show-debug-toolbar"]

class StudentTestCase(TestCase):
    """Test routs for students"""
    
    def setUp(self):
        db.drop_all()
        db.create_all()

        teacher = Teacher.seed_db(name="teacher_name", username="teacher", password="password")
        db.session.add(teacher)

        student = Student.seed_db(name="student_name", username="student", password="password", teacher_id=1)
        db.session.add(student)

        assignment = Assignment(title='title', body='body', teacher_id=1)
        db.session.add(assignment)

        one = StudentAssignment(assignment_id=assignment.id, student_id=student.id)
        db.session.add(one)

        db.session.commit()

    def tearDown(self):
        res = super().teachDown()
        db.session.rollback()
        return res

    def test_student_profile(self):
        """ Test /<student_id>/home with session set
        show this student's name, all assignments, and assignments as uncompleted
        Test /teacher/<teacher_id>/home 
        incorrect route for student even with same id, redirects because of session
        """
        with app.client as client:
            with client.session_transaction() as ses:
                ses["username"] = "student"

            res = client.get("/1/home")
            assign = StudentAssignment.query.all()

            self.assertIn("student_name", str(res.data))
            self.assertIn("title", str(res.data))
            self.assertFalse(assign[0].completed)
            self.assertEqual(len(assign), 1)

            r = cl.get("/teacher/1/home")

            self.assertEqual(r.status_code, 302)