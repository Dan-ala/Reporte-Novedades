from flask import Flask, jsonify, redirect,request,session,flash, url_for
from flask import render_template
import requests
from services.apicnx import Usuario

from flask import Blueprint

ambientes = Blueprint('ambientes', __name__, url_prefix='/ambientes',
                      template_folder='templates')


#AMBIENTES
@ambientes.route("/0", methods=["GET","POST"])
def index5():
    return render_template("ambientes.html", N="0")

@ambientes.route("/<id>", methods=["GET","POST"])
def learning_classroom(id=0):
    return render_template("ambientes.html", N=id)

@ambientes.route("test", methods = ["GET"])
def test():
    return "This is a test"


#LEARNIGN CLASSROOM LIST:
@ambientes.route("", methods=["GET"])
def AmbienteList():
    ambientes = Usuario("http://127.0.0.1:5000/ambientes")
    a = requests.get("http://127.0.0.1:5000/ambientes/to")
    aa = a.json()
    pue_tra = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    puesto_t = pue_tra.json()
    cadena = list (ambientes.ListarTodos())
    print (f"These are the desktops: \n{puesto_t}")
    classroom_workstations = [classroom[1] for classroom in aa]
    print (f"Workstations already registered: {classroom_workstations}")

    workstations_not_in_classroom = []
    msg = "No hay PTs para..."

    for workstation in puesto_t:
        if workstation[0] not in classroom_workstations:
            workstations_not_in_classroom.append(workstation)

    if workstations_not_in_classroom == []:
        msg = "No hay PTs para asignar."
    print(f"Workstations not in any learning classroom: {workstations_not_in_classroom}")

    return render_template("ambientes.html", N=0, cadena=cadena, puesto_t=workstations_not_in_classroom,msg=msg)


#NEW LEARNING CLASSROOM
@ambientes.route("i", methods=["POST"])
def LearningClassroomInsert():
    idPuestoTrabajo = request.form.get('idPuestoTrabajo')
    nombreAmbiente = request.form.get ('nombreAmbiente')
    ambi = Usuario("http://127.0.0.1:5000/ambientes")
    datos = {
        "idPuestoTrabajo": idPuestoTrabajo,
        "nombreAmbiente": nombreAmbiente
    }
    ambi.Inserte(datos)
    id=0
    msgitos = "Ambiente de formación creado"
    return render_template("alertas.html", msgito=msgitos)


#REGISTRO DE AMBIENTE DE FORMACION:
@ambientes.route("1", methods = ["GET","POST"])
def ambiente_record():
    response = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    puestos_t = response.json()
    return render_template("ambientes.html", N='1', puestos_t=puestos_t)


#ACTUALIZA AMBIENTE:
@ambientes.route("u", methods=["POST"])
def ActualizaAmbiente():
    id = request.form.get('id')
    idPuestoTrabajo=request.form.get('idPuestoTrabajo')
    nombreAmbiente=request.form.get('nombreAmbiente')
    ambi= Usuario("http://127.0.0.1:5000/ambientes")
    datos = {   
        "idAmbiente":id,
        "idPuestoTrabajo": idPuestoTrabajo,
        "nombreAmbiente": nombreAmbiente,
    }   
    ambi.Actualiza(datos)
    id=0
    msgitos = "Ambiente editado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

@ambientes.route("e/<id>", methods=["GET"])
def EditaAmbiente(id):
    ambi= Usuario("http://127.0.0.1:5000/ambientes")
    pue_tra = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    puesto_t = pue_tra.json()
    nombre_ambi = ambi.ListarUno(id)
    return render_template("ambientes.html", N=2, puesto_t=puesto_t, nombre_ambi=nombre_ambi)


#DELETE LEARNING CLASSROOMS:
@ambientes.route("d/<id>", methods = ["GET"])
def ambientesBorra(id):
    ambi = Usuario("http://127.0.0.1:5000/ambientes")
    cadena = ambi.Borra(id)
    msgitos = "Ambiente borrado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)