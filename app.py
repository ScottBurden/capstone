import os

from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from forms import LoginForm, GradeAssignmentForm
from models import Student, Teacher, Assignment, StudentAssignment, db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'postgresql:///capstone_school')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY","SECRET")
#TODO FILE TO IMPORT SECRET?


#if you want to turn off debug
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def landing_page():
    """Shows page where user selects to login as student or teacher, then redirects to that route
    """
    return render_template("landing.html")
 
#*************************Student only routes******************************

@app.route("/logout-student")
def remove_session():
    session.pop("username")
    flash("You are logged out", "success")
    return redirect("/login-student")

@app.route("/login-student", methods=["GET"])
def student_login():
    """Render page with form for student only login"""
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/login-student", methods=["POST"])
def authenticate_student():
    """Authenticate login form then redirects to their profile, returns error message for failed authentication,
    returns flash message for form not completed"""
    form = LoginForm()

    if form.validate_on_submit():
        usr = form.username.data
        pwd = form.password.data

        student = Student.authenticate(usr, pwd)
        
        if student:
            session["username"]=student.username
            return redirect(f"/{student.id}/home")
        
        else:
            form.username.errors = ["Login failed, please check your username and password"]
            return redirect("/login-student")

    else:
        flash("Please enter your username and password", "danger")
        return redirect("/login-student")


@app.route("/<int:s_id>/home", methods=["GET"])
def student_profile_page(s_id):
    student = Student.query.get_or_404(s_id)

    if student.username in session["username"]:
        work = Assignment.query.all()
        completed = StudentAssignment.query.filter_by(student_id=student.id).all()
        #TODO handle for student to complete hw POST to ("/<int:s_id>/hw/<int:a_id>")
    
        return render_template("student-profile.html", work=work, student=student, completed=completed)
    
    else:
        flash("You must be logged in to do that", "danger")
        return redirect("/login-student")


@app.route("/<int:s_id>/hw/<int:a_id>", methods=["GET"])
def show_assignment(s_id,a_id):
    """Display an individual assignment for the current student in session"""
    student = Student.query.get_or_404(s_id)

    if student.username in session["username"]:
        hw = Assignment.query.get_or_404(a_id)

        return render_template("hw.html", hw=hw, student=student)

    
    else:
        flash("You must be logged in to do that", "danger")
        return redirect("/login-student")

@app.route("/<int:s_id>/hw/<int:a_id>", methods=["POST"])
def finish_assignment(s_id,a_id):
    """Update "completed" boolean in students_assignments table for row with both student id and assignment id"""
    student = Student.query.get_or_404(s_id)

    if student.username in session["username"]:
        assign = Assignment.query.get_or_404(a_id)
        complete_assignment = StudentAssignment.query.filter_by(student_id=student.id, assignment_id=assign.id).first()
        complete_assignment.completed=True if not complete_assignment.completed else False

        db.session.add(complete_assignment)
        db.session.commit()       

        return redirect(f"/{student.id}/home")

    
    else:
        flash("You must be logged in to do that", "danger")
        return redirect("/login-student")


    
#*************************Teacher only routes************************

@app.route("/logout-teacher")
def remove_user_session():
    session.pop("username")
    flash("You are logged out", "success")
    return redirect("/login-teacher")

@app.route("/login-teacher", methods=["GET"])
def teacher_login():
    """Render page with form for teacher only login"""

    form = LoginForm()    
    return render_template("login.html", form=form)

@app.route("/login-teacher", methods=["POST"])
def authenticate_teacher():
    """Authenticate login from then redirects to their profile,
    returns error message for failed authentication, 
    returns flash message for form not completed"""    
    form = LoginForm()

    if form.validate_on_submit():
        usr = form.username.data
        pwd = form.password.data   
        teacher = Teacher.authenticate(usr, pwd)
        
        if teacher:
           session["username"]=teacher.username
           return redirect(f"/teacher/{teacher.id}/home")
        
        else:
           form.username.errors = ["Login failed, please check your username and password"]
           return redirect("/login-teacher")

    else:
        flash("Please enter your username and password", "danger")
        return redirect("/login-teacher")

@app.route("/teacher/<int:t_id>/home")
def teacher_profile_page(t_id):
    """Shows all students and all assignments"""
    teacher = Teacher.query.get_or_404(t_id)

    if teacher.username in session["username"]:

        students = Student.query.filter_by(teacher_id=t_id).all()
        work = Assignment.query.filter_by(teacher_id=t_id).all()
        completed = StudentAssignment.query.all()
    
        return render_template("teacher-profile.html", teacher=teacher, students=students, work=work, completed=completed)
    
    else:
        flash("You must be logged in to do that", "danger")
        return redirect("/login-teacher")


@app.route("/teacher/<int:t_id>/student/<int:s_id>")
def show_all_work(t_id, s_id):
    """Display all assignments with completion status for one student"""
    teacher = Teacher.query.get_or_404(t_id)

    if teacher.username in session["username"]:

        grade_form = GradeAssignmentForm()
        student = Student.query.get_or_404(s_id)
        assignments = db.session.query(Assignment.title, Assignment.id).all()
        completed = StudentAssignment.query.filter_by(student_id=student.id).all()
        
        return render_template("show-all.html", teacher=teacher, student=student, assignments=assignments, completed=completed, grade_form=grade_form)

    else:
        flash("You must be logged in to do that", "danger")
        return redirect("/login-teacher")

@app.route("/teacher/<int:t_id>/assignment/<int:a_id>")
def show_all_students(t_id, a_id):
    """Display all students and their completion status for one assignment"""
    teacher = Teacher.query.get_or_404(t_id)

    if teacher.username in session["username"]:

        grade_form = GradeAssignmentForm()
        assignment = Assignment.query.get_or_404(a_id)
        students = db.session.query(Student.name, Student.id).all()
        completed = StudentAssignment.query.filter_by(assignment_id=assignment.id).all()
        
        return render_template("show-all.html", teacher=teacher, assignment=assignment, students=students, completed=completed, grade_form=grade_form)

    else:
        flash("You must be logged in to do that", "danger")
        return redirect("/login-teacher")

@app.route("/teacher/<int:t_id>/grade/<int:sa_id>", methods=["POST"])
def grade_assignment(t_id,sa_id):
    """Receive grades submitted in GradeAssignmentForm, updated db and redirects to /home
    """
    form = GradeAssignmentForm()
    student_assignment = StudentAssignment.query.get(sa_id)

    if form.validate_on_submit():
        g = int(form.grade.data)
        student_assignment.grade = g
        db.session.add(student_assignment)
        db.session.commit()
        flash("Grade updated successfully!","primary")
        return redirect(f"/teacher/{t_id}/home")
    else:
        flash("Unable to save your submission, try again", "danger bg-warning")
        return redirect(f"/teacher/{t_id}/home")

#******************************DEMO ROUTE********************************
@app.route("/demo")
def show_preview():
    student = Student.query.get_or_404(9)
    work = Assignment.query.all()
    completed = StudentAssignment.query.filter_by(student_id=student.id).all()
    teacher = Teacher.query.get_or_404(1)
    works = Assignment.query.filter_by(teacher_id=1).all()
    t_completed = StudentAssignment.query.all()
    students = Student.query.filter(Student.id>8).all()
    
    return render_template("demo.html", student=student, work=work,completed=completed, teacher=teacher, works=works, t_completed=t_completed, students=students)
