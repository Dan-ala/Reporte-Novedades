from flask import Flask, jsonify, redirect,request,session,flash, url_for
from flask import render_template
import requests
from services.apicnx import Usuario


from flask import Blueprint

instructores_model = Blueprint('instructores', __name__, url_prefix='/instructores',
                      template_folder='templates')


#INSTRUCTORES
@instructores_model.route("/0",methods=["GET","POST"])
def index3():
    return render_template("instructores.html",N="0")

@instructores_model.route("/<id>", methods=["GET","POST"])
def instructores(id=0):
    return render_template("instructores.html",N=id)


#INSTRUCTOR LIST:
@instructores_model.route("", methods=["GET"])
def InstructorList():
    instructors = requests.get("http://127.0.0.1:5000/instructores")
    ambi = requests.get("http://127.0.0.1:5000/ambientes/to")
    t_instructors = requests.get("http://127.0.0.1:5000/tipo/instructor")
    cadena = instructors.json()
    cadena2 = ambi.json()
    tipo_inst = t_instructors.json()
    # print (f"Posicion 1: {cadena[0][1]}")
    print (f" Instructors: {cadena} \n and Learning Classrooms: {cadena2} \n and type of instructors: {tipo_inst}")
    can = len(cadena)

    #testing
    classrooms = [classroom[2] for classroom in cadena]
    print (f"Classrooms already taken by an instructor: {classrooms}")

    classrooms_not_designated = []
    msg = "No hay ambientes para..."

    for l_classroom in cadena2:
        if l_classroom[0] not in classrooms:
            classrooms_not_designated.append(l_classroom)

    print(f"Classrooms not designated: {classrooms_not_designated}")

    id=0
    return render_template("instructores.html", N=0, cadena=cadena,can=can,cadena2=cadena2,classrooms_not_designated=classrooms_not_designated,tipo_inst=tipo_inst,msg=msg)


#NEW INSTRUCTOR
@instructores_model.route("i", methods = ["POST"])
def InstructorsInsert():
    idTipoInstructor = request.form.get('idTipoInstructor')
    idAmbiente = request.form.get('idAmbiente')
    cedula = request.form.get('cedula')
    emailInstructor = request.form.get('emailInstructor')
    instructor = Usuario("http://127.0.0.1:5000/instructores")
    datos = {
        "idTipoInstructor": idTipoInstructor,
        "idAmbiente": idAmbiente,
        "cedula": cedula,
        "emailInstructor": emailInstructor
    }
    instructor.Inserte(datos)
    id=0
    msgitos = "Instructor creado"
    return render_template("alertas.html", msgito=msgitos)


#ACTUALIZA INSTRUCTOR:
@instructores_model.route("u", methods=["POST"])
def ActualizaInstructor():
    id = request.form.get('idInstructor')
    idTipoInstructor = request.form.get('idTipoInstructor')
    idAmbiente = request.form.get('idAmbiente')
    cedula = request.form.get('cedula')
    emailInstructor = request.form.get('emailInstructor')
    instructor = Usuario("http://127.0.0.1:5000/instructores")
    datos = {
        "idInstructor": id,
        "idTipoInstructor": idTipoInstructor,
        "idAmbiente": idAmbiente,
        "cedula": cedula,
        "emailInstructor": emailInstructor
    }
    print (f"Why None value \n: {instructor.Actualiza(datos)}")
    id=0
    msgitos = "Instructor editado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

@instructores_model.route("e/<id>", methods=["GET"])
def EditaInstructor(id):
    instructor = requests.get("http://127.0.0.1:5000/instructor/"+id)
    ambi = requests.get("http://127.0.0.1:5000/ambientes/to")
    cadena2 = ambi.json()
    t_instructor = requests.get("http://127.0.0.1:5000/tipo/instructor")
    tipo_inst = t_instructor.json()
    inst = instructor.json()
    
    print("Fetched instructor:", inst)  # Debug information
    if not inst:
        return "Instructor not found", 404

    return render_template("instructores.html", N=2, inst=inst, tipo_inst=tipo_inst, cadena2=cadena2)

#DELETE INSTRUCTORS:
@instructores_model.route("d/<id>", methods = ["GET"])
def instructoresBorra(id):
    instructores = Usuario("http://127.0.0.1:5000/instructores")
    cadena = instructores.Borra(id)
    msgitos = "Instructor borrado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

