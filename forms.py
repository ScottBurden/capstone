from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, NumberRange

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class GradeAssignmentForm(FlaskForm):

    grade = IntegerField("Grade", validators=[NumberRange(0,100)])
