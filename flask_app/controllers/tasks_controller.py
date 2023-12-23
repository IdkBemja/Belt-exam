from flask import Flask, render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.users import User
from flask_app.models.tasks import Task


@app.route("/new/task")
def new_task():
    if 'user_id' not in session:
        flash('Porfavor inicia sesión', 'not_in_session')
        return redirect('/')
    
    return render_template("new.html")


@app.route("/create/task", methods=["POST"])
def create_task():
    if 'user_id' not in session:
        flash('Porfavor inicia sesión', 'not_in_session')
        return redirect('/')
    
    if not Task.validate_task(request.form):
        return redirect("/new/task")
    
    Task.save(request.form)
    return redirect("/appointments")

@app.route("/edit/task/<int:id>")
def edit_task(id):
    if 'user_id' not in session:
        flash('Porfavor inicia sesión', 'not_in_session')
        return redirect('/')
    
    diccionario = {"id": id}
    task = Task.get_by_id(diccionario)

    return render_template('edit.html', task=task)

@app.route("/update/task", methods=["POST"])
def update_task():
    if 'user_id' not in session:
        flash('Porfavor inicia sesión', 'not_in_session')
        return redirect('/')
    if not Task.validate_task(request.form):
        return redirect("/edit/task/"+request.form["id"])
    
    Task.update(request.form)
    return redirect("/appointments")

@app.route("/delete/task/<int:id>")
def delete_task(id):
    if 'user_id' not in session:
        flash('Porfavor inicia sesión', 'not_in_session')
        return redirect('/')
    
    diccionario = {"id": id}
    Task.delete(diccionario)
    return redirect("/appointments")