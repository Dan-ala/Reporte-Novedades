from flask import Flask, jsonify, redirect,request
from flask import render_template
from flask_login import current_user, login_required
import requests
from services.apicnx import Usuario

from flask import Blueprint

puesto_trabajo = Blueprint('puesto_trabajo', __name__, url_prefix='/puesto_trabajo',
                      template_folder='templates')


#PUESTO_TRABAJO
@puesto_trabajo.route("/0",methods=["GET","POST"])
@login_required
def index2():
    return render_template("pt.html",N="0")

@puesto_trabajo.route("/<id>", methods=["GET","POST"])
@login_required
def pt(id=0):
    return render_template("pt.html",N=id)

#52
@puesto_trabajo.route("puestos/trabajo/add/elements/0", methods = ["GET","POST"])
@login_required
def index6():
    return render_template("pt.html", N="0")

@puesto_trabajo.route("puestos/trabajo/add/elements/<id>", methods=["GET","POST"])
@login_required
def l(id=0):
    return render_template("pt.html", N=id)


#NEW WORKSTATION
@puesto_trabajo.route("i", methods = ["POST"])
@login_required
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
@login_required
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
@login_required
def AddElementsToAWorkstation(idPuestoTrabajo):
    # Fetch elements assigned to the specific workstation
    response_puesto_trabajo = requests.get(f"http://127.0.0.1:5000/pt/{idPuestoTrabajo}")
    if response_puesto_trabajo.status_code != 200:
        return f"Error fetching workstation data: {response_puesto_trabajo.text}", 500
    
    current_workstation_elements = response_puesto_trabajo.json()

    # Extract IDs of elements assigned to the current workstation
    current_workstation_element_ids = {element[0] for element in current_workstation_elements}

    # Fetch all elements
    response_elements = requests.get("http://127.0.0.1:5000/usua/to")
    if response_elements.status_code != 200:
        return f"Error fetching elements data: {response_elements.text}", 500
    
    all_elements = response_elements.json()

    # Filter out elements that are already assigned to the current workstation
    elements_not_in_workstation = [element for element in all_elements if element[0] not in current_workstation_element_ids]
    
    msg = "No hay elementos para asignar." if not elements_not_in_workstation else "Seleccione los elementos para asignar."

    return render_template("pt.html", N=8, pts=current_workstation_elements, elements=elements_not_in_workstation, msg=msg)


#ACTUALIZA PT:
@puesto_trabajo.route("u", methods = ["POST"])
@login_required
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
@login_required
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
        print(f"ELEMENTS: \n {lucas}")
        cadena_dict = {item[0]: item[1] for item in elements}
        workstation_name = workstation[0][1] if workstation else "Unknown Workstation"
        return render_template(
            "pt.html", 
            N=0, 
            can=len(elements),
            cadena_dict=cadena_dict, 
            lucas=lucas,
            workstation_id=id, 
            workstation_name=workstation_name
        )
    else:
        return "Error: Failed to retrieve data from the endpoint"


#DESKTOP LIST:
@puesto_trabajo.route("", methods=["GET"])
@login_required
def DesktopList():
    desktops = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    cadena = desktops.json()
    can = len(cadena)

    # Fetch other necessary data
    response = requests.get("http://127.0.0.1:5000/usua/to2")
    response.raise_for_status()
    elementos = response.json()

    idInstructor = current_user.idInstructor  # Assuming this attribute exists on your User class
    idTipoInstructor = current_user.idTipoInstructor  # Assuming this attribute exists on your User class

    print (f"Current user: {idTipoInstructor}")

    if idTipoInstructor == 1:  # If the user is an accountant
        instructors_by_idAmbiente_response = requests.get(f"http://127.0.0.1:5000/instructores/ambientes/{idInstructor}")
        clss_by_an_instructor = instructors_by_idAmbiente_response.json()
        print(f"Learning classrooms that belong to an accountant: \n{clss_by_an_instructor}")

        ambientes_response = requests.get("http://127.0.0.1:5000/ambientes/add/pts")
        ambiente_puesto = ambientes_response.json()
        print(f"Ambiente Puesto: {ambiente_puesto}")

        instructor_pt_response = requests.get("http://127.0.0.1:5000/ambientes/pts")
        i = instructor_pt_response.json()
        print(f"Initial Workstations List (i): {i}")

        novelties_response = requests.get("http://127.0.0.1:5000/novedades")  # Adjust the endpoint as needed
        novelties = novelties_response.json()
        print(f"Novelties: {novelties}")

        # List to hold matching workstations with novelty status
        matching_workstations = []

        # Loop through each classroom that belongs to the instructor
        for classroom in clss_by_an_instructor:
            idInstructor_classroom = classroom[0]  # idInstructor from the classroom list
            idAmbiente = classroom[1]  # idAmbiente from the classroom list

            # Check against each workstation
            for workstation in i:
                ws_idAmbiente = workstation[0]  # idAmbiente from the workstation list
                ws_idPuestoTrabajo = workstation[1]  # idPuestoTrabajo from the workstation list

                if idAmbiente == ws_idAmbiente:
                    # Find the name of the puesto trabajo
                    ws_name = next((x[3] for x in ambiente_puesto if x[2] == ws_idPuestoTrabajo), None)
                    # Check if this puesto trabajo has a novelty
                    has_novelty = any(novelty[1] == ws_idPuestoTrabajo for novelty in novelties)
                    matching_workstations.append((idInstructor_classroom, ws_idPuestoTrabajo, ws_name, has_novelty))
                    print(f"Workstation that belongs to {idInstructor_classroom}: {ws_name} {'(Novelty)' if has_novelty else ''}")

        print(f"Filtered Workstations List (matching_workstations): {matching_workstations}")
        return render_template("pt.html", N=7, cadena=cadena, can=can, elementos=elementos, ws_idPuestoTrabajo=matching_workstations)

    else:  # If the user is an admin
        print(f"Admin Workstations List: {cadena}")
        return render_template("pt.html", N=7, cadena=cadena, can=can, elementos=elementos, ws_idPuestoTrabajo=cadena)



#REGISTRO DE PUESTO DE TRABAJO:
@puesto_trabajo.route("1", methods = ["GET","POST"])
@login_required
def pt_record():
    response = requests.get("http://127.0.0.1:5000/usua/to2")
    elementos = response.json()
    return render_template("./pt/pt.html")


#DELETE WORKSTATIONS:
@puesto_trabajo.route("d/<id>", methods = ["GET"])
@login_required
def puestosTrabajoBorra(id):
    pts = Usuario("http://127.0.0.1:5000/puesto_trabajo")
    cadena = pts.Borra(id)
    msgitos = "Puesto de Trabajo borrado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)