# imports
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

#Here we are gonna import the bluprints
from ambientes.routes import ambientes
from menu.routes import menu
from novedades.routes import novedades
from puesto_trabajo.routes import puesto_trabajo
from instructores.routes import instructores_model
from elementos.routes import elementos
import requests

from services.apicnx import UsuarioLogin

from flask_mail import Mail
import requests

mail = Mail()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config.from_object('config.Config')

    mail.init_app(app)

    login_manager.init_app(app)  # Initialize LoginManager with the app
    login_manager.login_view = 'login'  # Set the default login view
    
    CORS(app)
    app.register_blueprint(ambientes)
    app.register_blueprint(menu)
    app.register_blueprint(novedades)
    app.register_blueprint(puesto_trabajo)
    app.register_blueprint(instructores_model)
    app.register_blueprint(elementos)


    return app

@login_manager.user_loader
def load_user(user_id):
    response = requests.get(f"http://127.0.0.1:5000/instructores")
    instructors = response.json()
    
    for instructor in instructors:
        if instructor[0] == int(user_id):
            return UsuarioLogin(instructor)
    return None