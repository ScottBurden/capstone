from app import app
from models import db, Teacher, Student, Assignment, StudentAssignment

db.drop_all()
db.create_all()

scott = Teacher.seed_db(name="burden", username="scottb", password="password")

db.session.add(scott)
db.session.commit()

s = Teacher.query.get(1)

s0 = Student.seed_db(name="John A", username="johna", password="psswrd", teacher_id=1)
s1 = Student.seed_db(name="John B", username="johnb", password="psswrd", teacher_id=1)
s2 = Student.seed_db(name="John C", username="johnc", password="psswrd", teacher_id=1)
s3 = Student.seed_db(name="John D", username="johnd", password="psswrd", teacher_id=1)
s4 = Student.seed_db(name="John E", username="johne", password="psswrd", teacher_id=1)
s5 = Student.seed_db(name="John F", username="johnf", password="psswrd", teacher_id=1)
s6 = Student.seed_db(name="John H", username="johnh", password="psswrd", teacher_id=1)
s7 = Student.seed_db(name="John I", username="johni", password="psswrd", teacher_id=1)
s8 = Student.seed_db(name="John J", username="johnj", password="psswrd", teacher_id=1)
s9 = Student.seed_db(name="John K", username="johnk", password="psswrd", teacher_id=1)

db.session.add_all([s0, s1, s2, s3, s4, s5, s6, s7, s8, s9])
db.session.commit()


a0 = Assignment(title="hw 1", body="hw", teacher_id=1)
a1 = Assignment(title="hw 2", body="hw", teacher_id=1)
a2 = Assignment(title="hw 3", body="hw", teacher_id=1)
a3 = Assignment(title="hw 4", body="hw", teacher_id=1)
a4 = Assignment(title="hw 5", body="hw", teacher_id=1)
a5 = Assignment(title="hw 6", body="hw", teacher_id=1)
a6 = Assignment(title="hw 7", body="hw", teacher_id=1)
a7 = Assignment(title="hw 8", body="hw", teacher_id=1)
a8 = Assignment(title="hw 9", body="hw", teacher_id=1)
a9 = Assignment(title="final", body="hw", teacher_id=1)

db.session.add_all([a0, a1, a2, a3, a4, a5, a6, a7, a8, a9])
db.session.commit()

student = Student.query.all()
assign = Assignment.query.all()
all_assign = []
for st in student:
    for asn in assign:
        one = StudentAssignment(assignment_id=asn.id, student_id=st.id)
        all_assign.append(one)

db.session.add_all(all_assign)
db.session.commit()
