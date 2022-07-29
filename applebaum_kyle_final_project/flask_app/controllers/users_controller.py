from flask_app.models.user_model import User
from flask_app.models.project_model import Project

from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sign_up')
def signup():
    return render_template("register.html")


@app.route('/process', methods=['POST'])
def process():
    if not User.is_valid(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/sign_in', methods=['POST'])
def signin():
    user = User.email_request(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def result():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.id_request(data), all_projects=Project.get_all())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
