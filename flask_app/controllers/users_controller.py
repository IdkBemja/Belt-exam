from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

from datetime import datetime

from flask_app.models.users import User
from flask_app.models.tasks import Task

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')    
    pass_encrypt = bcrypt.generate_password_hash(request.form['password'])
    form = {
        "name": request.form['name'],
        "email": request.form['email'],
        "password": pass_encrypt
    }

    id = User.save(form)
    session['user_id'] = id
    return redirect('/appointments')

@app.route('/appointments')
def dashboard():
    if 'user_id' not in session:
        flash('Porfavor inicia sesión', 'not_in_session')
        return redirect('/')
    form = {"id": session['user_id']}
    user = User.get_by_id(form)
    tasks = Task.get_all()
    return render_template('dashboard.html', user=user, tasks=tasks, now=datetime.now)

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash('E-mail no registrado', 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/appointments')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')