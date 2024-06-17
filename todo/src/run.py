# This app refer to the app folder
#     ⇩
from flask import flash, redirect, request, render_template, session, url_for
from app import create_app
from services.apicnx import Usuario
from flask_mail import Mail, Message
import requests

# This app refer to the flask app
# ⇩
app = create_app() # CREATE THE FLASK APP

#VALIDANDO LAS RUTAS


#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        r = requests.get("http://127.0.0.1:5000/instructores")
        cedula = int(request.form.get("cedula"))
        emailInstructor = request.form.get("emailInstructor")
        rs = r.json()
        print (rs)

        found = False
        for x in rs:
            
            if cedula == x[2] and emailInstructor == x[3] and x[1] == 1:
                session["cedula"] = cedula
                session["emailInstructor"] = emailInstructor
                found = True
                break
            elif cedula == x[2] and emailInstructor == x[3] and x[1] == 2:
                flash(f"El instructor con cc: {x[2]} NO es un cuentadante.")
                return redirect(url_for('login'))
        if found:
            return redirect("/menu")
        else:
            flash("Cédula o E-mail incorrectos")
            return redirect(url_for('login'))
        
    return render_template("login.html", error=error)

if __name__ == '__main__':
    app.run(debug = True, port = 8000, host='0.0.0.0')