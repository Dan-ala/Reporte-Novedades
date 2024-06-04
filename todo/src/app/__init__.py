# imports
from flask import Flask, request, render_template
from flask_cors import CORS

#Here we are gonna import the bluprints
from ambientes.routes import ambientes
from menu.routes import menu
from novedades.routes import novedades
from puesto_trabajo.routes import puesto_trabajo
from instructores.routes import instructores_model
from elementos.routes import elementos
import requests

from services.apicnx import Usuario

from flask_mail import Mail, Message
import requests

mail = Mail()

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config.from_object('config.Config')

    mail.init_app(app)   
    
    CORS(app)
    app.register_blueprint(ambientes)
    app.register_blueprint(menu)
    app.register_blueprint(novedades)
    app.register_blueprint(puesto_trabajo)
    app.register_blueprint(instructores_model)
    app.register_blueprint(elementos)


    return app