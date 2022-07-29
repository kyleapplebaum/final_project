from flask_app.models.project_model import Project
from flask_app.models.user_model import User

from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash


@app.route('/project/new')
def new_project():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('new_project.html', user=User.id_request(data))


@app.route('/project/create', methods=['POST'])
def create_project():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Project.validate_project(request.form):
        return redirect('/project/new')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Project.save(data)
    return redirect('/dashboard')


@app.route('/project/edit/<int:id>')
def edit_project(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit_project.html", project=Project.get_one(data), user=User.id_request(user_data))


@app.route('/project/update', methods=['POST'])
def update_project():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Project.validate_project(request.form):
        return redirect('/project/edit/<int:id>')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "id": request.form['id']
    }
    Project.update(data)
    return redirect('/dashboard')


@app.route('/project/<int:id>')
def show_project(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("project.html", project=Project.get_one(data), user=User.id_request(user_data))


@app.route('/project/delete/<int:id>')
def delete_project(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Project.delete(data)
    return redirect('/dashboard')
