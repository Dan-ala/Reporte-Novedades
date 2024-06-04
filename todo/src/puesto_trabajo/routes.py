from flask import Flask, jsonify, redirect,request,session,flash, url_for
from flask import render_template
import requests
from services.apicnx import Usuario

from flask import Blueprint

puesto_trabajo = Blueprint('puesto_trabajo', __name__, url_prefix='/puesto_trabajo',
                      template_folder='templates')


#PUESTO_TRABAJO
@puesto_trabajo.route("/0",methods=["GET","POST"])
def index2():
    return render_template("pt.html",N="0")

@puesto_trabajo.route("/<id>", methods=["GET","POST"])
def pt(id=0):
    return render_template("pt.html",N=id)

#52
@puesto_trabajo.route("puestos/trabajo/add/elements/0", methods = ["GET","POST"])
def index6():
    return render_template("pt.html", N="0")

@puesto_trabajo.route("puestos/trabajo/add/elements/<id>", methods=["GET","POST"])
def l(id=0):
    return render_template("pt.html", N=id)


#NEW WORKSTATION
@puesto_trabajo.route("i", methods = ["POST"])
def WorkstationInsert():
    nombrePT = request.form.get('nombrePT')
    workstation = Usuario("http://127.0.0.1:5000/puesto_trabajo")
    datos = {
        "nombrePT": nombrePT,
    }
    workstation.Inserte(datos)
    id = 0
    msgitos = "Puesto de Trabajo creado"
    return render_template("alertas.html", msgito=msgitos)

#ADD ELEMENTS TO A WORKSTATION:
@puesto_trabajo.route("puestos/trabajo/add/elements/i", methods = ["POST"])
def add_elements():
    idPuestoTrabajo = request.form.get("idPuestoTrabajo")
    idElemento = request.form.get("idElemento")
    workstation = Usuario("http://127.0.0.1:5000/puestos/trabajo/add/elements")
    datos = {
        "idPuestoTrabajo": idPuestoTrabajo,
        "idElemento": idElemento
    }
    workstation.Inserte(datos)
    id=0
    msgitos = "Elemento agregado"
    return render_template("alertas.html", msgito=msgitos)



#ADD ELEMENTS TO A WORKSTATION
@puesto_trabajo.route("ptrabajo/add/elements/<idPuestoTrabajo>", methods = ["GET"])
def AddElementsToAWorkstation(idPuestoTrabajo):
    puesto_trabajo = requests.get("http://127.0.0.1:5000/puestos/trabajo/"+idPuestoTrabajo)
    ele = requests.get("http://127.0.0.1:5000/usua/to")
    elements = ele.json()
    pts = puesto_trabajo.json()
    print(f"PTs: \n {pts}")
    print (f"Elements to add: \n {elements}")
    return render_template("pt.html", N=8, pts=pts, elements=elements)


#ACTUALIZA PT:
@puesto_trabajo.route("u", methods = ["POST"])
def ActualizaPT():
    id = request.form.get("idPuestoTrabajo")
    nombrePT = request.form.get("nombrePT")
    workstation = Usuario("http://127.0.0.1:5000/puesto_trabajo")
    datos = {
        "idPuestoTrabajo": id,
        "nombrePT": nombrePT
    }
    workstation.Actualiza(datos)
    id=0
    msgitos = "Puesto de Trabajo editado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

@puesto_trabajo.route("e/<id>", methods = ["GET"])
def EditaPT(id):
    workstation = requests.get("http://127.0.0.1:5000/puestos/trabajo/" + id)
    one_workstation = workstation.json()
    print (one_workstation)
    return render_template("pt.html", N=2, one_workstation=one_workstation)


#PT
@puesto_trabajo.route("pt/<id>", methods=["GET"])
def lulo(id):
    response = requests.get("http://127.0.0.1:5000/pt/" + id)
    r = requests.get("http://127.0.0.1:5000/puestos/trabajo/" + id)
    workstation = r.json()
    print(f"This is your workstation: \n {workstation}")
    lucas = response.json()
    if response.status_code == 200:
        elements = response.json()
        print(f"ELEMENTS: \n {elements}")
        cadena_dict = {item[0]: item[1] for item in elements}
        workstation_name = workstation[0][1] if workstation else "Unknown Workstation"
        return render_template(
            "pt.html", 
            N=0, 
            can=len(elements), 
            cadena=elements, 
            cadena_dict=cadena_dict, 
            lucas=lucas,
            workstation_id=id, 
            workstation_name=workstation_name
        )
    else:
        return "Error: Failed to retrieve data from the endpoint"


#DESKTOP LIST:
@puesto_trabajo.route("",methods=["GET"])
def DesktopList():
    desktops= requests.get("http://127.0.0.1:5000/puestos/trabajo")
    cadena = desktops.json()
    can=len(cadena)

    response = requests.get("http://127.0.0.1:5000/usua/to2")
    elementos = response.json()
    id=0
    return render_template("pt.html",N=7,cadena=cadena,can=can,elementos=elementos)


#REGISTRO DE PUESTO DE TRABAJO:
@puesto_trabajo.route("1", methods = ["GET","POST"])
def pt_record():
    response = requests.get("http://127.0.0.1:5000/usua/to2")
    elementos = response.json()
    return render_template("./pt/pt.html")


#DELETE WORKSTATIONS:
@puesto_trabajo.route("d/<id>", methods = ["GET"])
def puestosTrabajoBorra(id):
    pts = Usuario("http://127.0.0.1:5000/puesto_trabajo")
    cadena = pts.Borra(id)
    msgitos = "Puesto de Trabajo borrado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)