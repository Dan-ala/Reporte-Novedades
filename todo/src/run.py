# This app refer to the app folder
#     ⇩
from flask import request, render_template
from app import create_app
from services.apicnx import Usuario
from flask_mail import Mail, Message
import requests

# This app refer to the flask app
# ⇩
app = create_app() # CREATE THE FLASK APP

if __name__ == '__main__':
    app.run(debug = True, port = 8000, host='0.0.0.0')