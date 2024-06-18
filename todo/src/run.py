# This app refer to the app folder
#     ⇩
from flask import flash, redirect, request, render_template, session, url_for
from app import create_app
from services.apicnx import Usuario, UsuarioLogin
from flask_mail import Mail, Message
import requests

from flask_login import LoginManager, login_user, login_required, logout_user

# This app refer to the flask app
# ⇩
app = create_app() # CREATE THE FLASK APP

#VALIDANDO LAS RUTAS

#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        response = requests.get("http://127.0.0.1:5000/instructores")
        instructors = response.json()

        cedula = int(request.form.get("cedula"))
        emailInstructor = request.form.get("emailInstructor")

        found = False
        for instructor in instructors:
            if len(instructor) >= 4 and cedula == instructor[2] and emailInstructor == instructor[3]:
                if instructor[1] == 1:  # Check if instructor type is suitable for login
                    user = UsuarioLogin([instructor[0], instructor[1], instructor[2], instructor[3]])
                    login_user(user)  # Log in the user
                    found = True
                    break
                else:
                    flash(f"El instructor con cc: {instructor[2]} NO es un cuentadante.")
                    return redirect(url_for('login'))
        
        if found:
            return redirect(url_for('menu.lista'))  # Redirect to the menu after successful login
        else:
            flash("Cédula o E-mail incorrectos")
            return redirect(url_for('login'))

    return render_template("login.html", error=error)


@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect (url_for('login'))

if __name__ == '__main__':
    app.run(debug = True, port = 8000, host='0.0.0.0')