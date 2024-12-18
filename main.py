from flask import Flask, render_template, request, redirect, url_for
from forms import UserForm
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5

import secrets
from models import User

app = Flask(__name__)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)


foo = secrets.token_urlsafe(16)
app.secret_key = foo

users=[]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def show_users():
    return render_template('users/users.html', users=users)

@app.route('/user', methods=['GET', 'POST'])
def show_user_form():
    if request.method == 'GET':
        form = UserForm()
        return render_template('users/user.html', form=form)
    if request.method == 'POST':
        form = UserForm()
        if form.validate_on_submit():
            user = User(form.id.data,form.firstname.data, form.lastname.data, form.email.data, form.birth_year.data)
            users.append(user)
            print(users)
            return redirect(url_for("show_users", users=users))
        else:
            return render_template('users/user.html', form=form)


@app.route('/user/<int:id>')
def show_user(id):
    found=False
    for user in users:
        if user.id == id:
            found
            form = UserForm(obj=user)
            return render_template('users/user.html',form=form)
    if not found:
        return render_template('users/users.html',users=users, message="User not found")
