from flask import Flask, jsonify,request,redirect, url_for
import json,requests
from flask import render_template
from services.apicnx import Usuario   
    
app=Flask(__name__)

@app.route("/niveles/0",methods=["GET","POST"])
def index():
    return render_template("niveles.html",N="0")

@app.route("/niveles/<id>",methods=["GET","POST"])
def nivel(id=0):
    return render_template("niveles.html",N=id)

@app.route("/niveles/i",methods=["POST"])
def nivelInserta():
    nom=request.form.get('nom')
    ape=request.form.get('ape')
    u1= Usuario("http://127.0.0.1:5000/usua")
    
    
    datos={
        "NOMBRE":nom,"APELLIDO":ape
    }
    u1.Inserte(datos)
    id=0
    msgitos="Usuario creado satisfactoriamente"
    return render_template("alertas.html",msgito=msgitos)

@app.route("/niveles/u",methods=["POST"])
def nivelactualiza():
    id=request.form.get('id')
    nom=request.form.get('nom')
    ape=request.form.get('ape')
    u1= Usuario("http://127.0.0.1:5000/usua")
    datos={
        "IDUSUARIO":id,"NOMBRE":nom,"APELLIDO":ape
    }
    u1.Actualiza(datos)
    id=0
    msgitos="Usuario editado satisfactoriamente"
    return render_template("alertas.html",msgito=msgitos)


@app.route("/niveles/e/<id>",methods=["GET"])
def nivelEdita(id):
    u1= Usuario("http://127.0.0.1:5000/usua")
    cadena=u1.ListarUno(id)
    return render_template("niveles.html",N=2,cadena=cadena)
@app.route("/niveles/d/<id>",methods=["GET"])
def nivelBorra(id):
    u1= Usuario("http://127.0.0.1:5000/usua")
    cadena=u1.Borra(id)
    msgitos="Usuario borrado satisfactoriamente"
    return render_template("alertas.html",msgito=msgitos)


@app.route("/niveles/r",methods=["POST"])
def Lista():
    u1= Usuario("http://127.0.0.1:5000/usua")
    cadena=u1.ListarTodos()
    can=len(cadena)
    id="0"
    return cadena
    return render_template("niveles.html",N=id,cadena=cadena,can=len(cadena))

@app.route("/niveles/l",methods=["GET"])
def ListarTodos():
    u1= Usuario("http://127.0.0.1:5000/usua")
    cadena=list(u1.ListarTodos())
    can=len(cadena)
    id=0
    return render_template("niveles.html",N=id,cadena=cadena,can=can)
    

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)    
    