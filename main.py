from flask import Flask, render_template, request, redirect, url_for
from forms import UserForm, JobForm, CourseForm, EnrollForm
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5
import os
import psycopg2
import secrets
from models import User, Job, Course
from database import (get_db_connection, init_db,
                      get_users, save_user, get_user, delete_user, edit_user,
                      get_jobs, get_user_jobs, save_job_user, get_courses, get_course,
                      save_course, enroll_users_to_course, get_user_courses)
app = Flask(__name__)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)




foo = secrets.token_urlsafe(16)
app.secret_key = foo

users=[]

#initialize the database
init_db()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def show_users():
    users = get_users()
    print(users)
    return render_template('users/users.html', users=users)

@app.route('/courses')
def show_courses():
    courses = get_courses()
    print(users)
    return render_template('courses/courses.html', courses=courses)

@app.route('/jobs')
def show_jobs():
    jobs = get_jobs()
    print(jobs)
    return render_template('jobs/jobs.html', jobs=jobs)

@app.route('/jobs/<int:id>')
def show_user_jobs(id):
    jobs = get_user_jobs(id)
    print(jobs)
    return render_template('jobs/jobs.html', jobs=jobs)

@app.route('/addjob/<int:id>', methods=['GET','POST'])
def add_job_to_user(id):
    user = get_user(id)
    if user:
        if request.method == 'GET':
            form = JobForm(user_id=id)
            return render_template('jobs/job.html', form=form, user=user)
        if request.method == 'POST':
            form = JobForm(user_id=id)
            if form.validate_on_submit():
                job = Job(form.name.data, form.description.data, id)
                save_job_user(job, id)
                return redirect(url_for("show_user_jobs", id=id))
            else:
                return render_template('jobs/job.html', form=form, user=user)
    else:
        return render_template('users/users.html',users=users, message="User not found")



@app.route('/user', methods=['GET', 'POST'])
def show_user_form():
    if request.method == 'GET':
        form = UserForm()
        return render_template('users/user.html', form=form)
    if request.method == 'POST':
        form = UserForm()
        if form.validate_on_submit():
            user = User(form.firstname.data, form.lastname.data, form.email.data, form.birth_year.data)
            save_user(user)
            print(users)
            return redirect(url_for("show_users", users=users))
        else:
            return render_template('users/user.html', form=form)

@app.route('/showuser/<int:id>')
def show_user_from_db(id):
    found=False
    user = get_user(id)
    if user:
        return render_template('users/user-details.html', user=user)
    else:
        return render_template('users/users.html',users=users, message="User not found")

@app.route('/user/<int:id>')
def show_user(id):
    found=False
    user = get_user(id)
    if user:
        form = UserForm(obj=user)
        return render_template('users/user.html', form=form)
    else:
        return render_template('users/users.html',users=users, message="User not found")

@app.route('/user/<int:id>', methods=['POST'])
def edit_user_post(id):
    form = UserForm()
    user = get_user(id)
    if user:
        print(user)
        changed_user = User(form.firstname.data, form.lastname.data, form.email.data, form.birth_year.data)
        edit_user(changed_user,id)
        users = get_users()
        return render_template('users/users.html', users=users, message="User changed")
    else:
        users = get_users()
        return render_template('users/users.html', users=users, message="User not found")
@app.route('/deleteuser/<int:id>')
def delete_user_from_db(id):
    found=False
    result = delete_user(id)
    print(result)
    users = get_users()
    if result:
        return render_template('users/users.html', users=users, message="User deleted")
    else:
        return render_template('users/users.html', users=users, message="User not found")

@app.route('/course', methods=['GET', 'POST'])
def show_course_form():
    if request.method == 'GET':
        form = CourseForm()
        return render_template('courses/course.html', form=form)
    if request.method == 'POST':
        form = CourseForm()
        courses = get_courses()
        if form.validate_on_submit():
            course = Course(form.name.data, form.description.data)
            save_course(course)
            print(users)
            return redirect(url_for("show_courses", courses=courses))
        else:
            return render_template('users/user.html', form=form)

@app.route('/course/<int:id>/users')
def show_course_users(id):
    course = get_course(id)
    users = get_user_courses(id)
    if course:
        return render_template('users/users.html', id=id, course=course, users=users)

@app.route('/enroll/<int:id>', methods=['GET', 'POST'])
def enroll_users(id):
    course = get_course(id)
    users = get_users()
    if course:
        form = EnrollForm(course_id=id)
        form.user_id.choices = [(user.id, user.firstname + ' ' + user.lastname) for user in users]
        if request.method == 'GET':
            return render_template('courses/enroll.html', id=id, course=course, form=form)
        if request.method == 'POST':
            if form.validate_on_submit():
                selected_users = form.user_id.data
                for user_id in selected_users:
                    enroll_users_to_course(user_id, id)
                print(selected_users)
                return render_template('courses/courses.html', id=id, course=course)