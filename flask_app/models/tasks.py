from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Task:

    db = "examen_python"

    def __init__(self, data):
        self.id = data["id"]
        self.task_name = data["task_name"]
        self.date = data["date"]
        self.status = data["status"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        # Ver Quien califico

       # self.first_name = data["first_name"] # 2 Variables creadas para mostrar el nombre del teacher (Nombre)
       # self.last_name = data["last_name"] # 2 Variables creadas para mostrar el nombre del teacher (Apellido)

       #self.teacher = data["first_name"] + " " + data["last_name"] # Una sola variable creada para mostrar el nombre del teacher

    @staticmethod
    def validate_task(form):
        is_valid = True

        if form["task_name"] == '':
            flash("La tarea no puede estar vacia", "tasks")
            is_valid = False
            
        if form["date"] == '':
            flash("Ingresa una fecha", "tasks")
            is_valid = False
        else:
            fecha_tarea = datetime.strptime(form["date"], "%Y-%m-%d")
            hoy = datetime.now()
            if hoy < fecha_tarea:
                flash("La fecha no puede ser futura.", "tasks")
                is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, form):
        query = "INSERT INTO tasks (task_name, date, status, user_id) VALUES (%(task_name)s, %(date)s, %(status)s, %(user_id)s)"
        result = connectToMySQL(Task.db).query_db(query, form)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tasks"
        results = connectToMySQL(Task.db).query_db(query)
        tasks = []
        for task in results:
            tasks.append(cls(task))
        return tasks
    
    @classmethod
    def get_by_id(cls, form):
        query = "SELECT * FROM tasks WHERE id = %(id)s"
        result = connectToMySQL(Task.db).query_db(query, form)
        task = cls(result[0])
        return task
    
    @classmethod
    def update(cls, form):
        query = "UPDATE tasks SET task_name=%(task_name)s, date=%(date)s, status=%(status)s WHERE id=%(id)s"
        result = connectToMySQL(Task.db).query_db(query, form)
        return result
    
    @classmethod
    def delete(cls, form):
        query = "DELETE FROM tasks WHERE id = %(id)s"
        result = connectToMySQL(Task.db).query_db(query, form)
        return result