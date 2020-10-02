# Classroom Cubby
**where students and teachers come together remotely**

[Check out the demo page!](https://classroom-cubby.herokuapp.com/demo)

This platform is designed for teachers to assign a class of students work that can be completed at their own pace. 

### Teacher Profile

The Teacher can see every student on their home page along with every assignment. Teachers can also filter by assignment or student to see all related info. It is updated in real time to show which students have completed which assignments. Uncompleted work displays as blue and completed work shows up green. After a student has completed an assignment on their profile, it will appear on the teacher's page immediately as completed while also adding a place to input a grade. Grades are stored, then returned to the student's profile. The Teacher's profile is protected with a username and password login, and special authorization to insure their identity.

### Student Profile

The Student has a secure login to protect their profile, while additional authorization is added to keep students from viewing each other's profiles. Same goes for the Teacher's profile, no peeking! Students are able to see all assignments given to them, and click into each individually to display a full description of the work then complete it. When a teacher has graded a completed assignment, the grade shows up on the student's profile as well.

For this set up, assignments were requested from an API for poems [PoetryDB](https://poetrydb.org/index.html)

### Technology stack:
database - PostgresQL

server - python Flask, also deployed on Heroku

Code includes Jinja templates, WTForms to prevent cross site request forgery, Bcrypt for authentication and secure storage of hashed passwords, no plaintext

SQLAlchemy for managing database from Flask

CSS Bootstrap


Testing coverage includes db models, routes, view functions, and authorization.
