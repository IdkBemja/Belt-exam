#Terminal: pipenv install flask pymysql flask-bcrypt
from flask_app import app
from flask_app.controllers import users_controller, tasks_controller


if __name__ == "__main__":
    app.run(debug=True)