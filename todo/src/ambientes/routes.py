from flask import Flask, jsonify, redirect,request,session,flash, url_for
from flask import render_template
import requests
from services.apicnx import Usuario

from flask import Blueprint

from flask_login import current_user, login_required

ambientes = Blueprint('ambientes', __name__, url_prefix='/ambientes',
                      template_folder='templates')


#AMBIENTES
@ambientes.route("/0", methods=["GET","POST"])
@login_required
def index5():
    return render_template("ambientes.html", N="0")

@ambientes.route("/<id>", methods=["GET","POST"])
@login_required
def learning_classroom(id=0):
    return render_template("ambientes.html", N=id)


# LEARNING CLASSROOM STATUS
@ambientes.route("estado/<idAmbiente>", methods=["GET"])
def test(idAmbiente):
    try:
        # Fetch data for the given idAmbiente
        ambiente_puesto_id = requests.get(f"http://127.0.0.1:5000/ambientes/pts/{idAmbiente}")
        ambiente_puesto_id.raise_for_status()
        d = ambiente_puesto_id.json()
        print(f"ambiente puesto_id: {d}")

        ambientes_response = requests.get("http://127.0.0.1:5000/ambientes/add/pts")
        ambientes_response.raise_for_status()
        ambiente_puesto = ambientes_response.json()

        ambi = requests.get("http://127.0.0.1:5000/ambientes").json()

        cadena_dict = {item[0]: item[1] for item in ambi}

        novelties_response = requests.get("http://127.0.0.1:5000/novedades")
        novelties_response.raise_for_status()
        novelties = novelties_response.json()

        matching_workstations = []

        for workstation in d:
            ws_idPuestoTrabajo = workstation[1]
            ws_name = next((x[3] for x in ambiente_puesto if x[2] == ws_idPuestoTrabajo), None)
            has_novelty = any(novelty[1] == ws_idPuestoTrabajo for novelty in novelties)
            matching_workstations.append((ws_idPuestoTrabajo, ws_name, has_novelty))
            print(f"Workstation that belongs to {ws_name} {'(Novelty)' if has_novelty else ''}")

        print("DATA:", matching_workstations)

        return render_template("estado_ambientes.html", ambiente_puesto=ambiente_puesto, ws_idPuestoTrabajo=matching_workstations, cadena_dict=cadena_dict)
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return "Error occurred during processing.", 500



# LEARNING CLASSROOM STATUS
@ambientes.route("estado", methods=["GET"])
def testxx():
    idInstructor = current_user.idInstructor
    instructors_by_idAmbiente_response = requests.get(f"http://127.0.0.1:5000/instructores/ambientes/{idInstructor}")
    clss_by_an_instructor = instructors_by_idAmbiente_response.json()
    print(f"Learning classrooms that belong to an accountant: \n{clss_by_an_instructor}")

    ambientes_response = requests.get("http://127.0.0.1:5000/ambientes/add/pts")
    ambiente_puesto = ambientes_response.json()
    print(ambiente_puesto)

    instructor_pt_response = requests.get("http://127.0.0.1:5000/ambientes/pts")
    i = instructor_pt_response.json()
    print(i)

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

    return render_template("estado_ambientes.html", ambiente_puesto=ambiente_puesto, ws_idPuestoTrabajo=matching_workstations)














#LEARNIGN CLASSROOM LIST:
@ambientes.route("", methods=["GET"])
@login_required
def AmbienteList():
    ambientes = Usuario("http://127.0.0.1:5000/ambientes")
    a = requests.get("http://127.0.0.1:5000/ambientes/to")
    aa = a.json()
    pue_tra = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    puesto_t = pue_tra.json()

    puesto_elemento = requests.get("http://127.0.0.1:5000/puestos/trabajo/add/elements")
    pp = puesto_elemento.json()

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
@login_required
def LearningClassroomInsert():
    nombreAmbiente = request.form.get ('nombreAmbiente')
    ambi = Usuario("http://127.0.0.1:5000/ambientes")
    datos = {
        "nombreAmbiente": nombreAmbiente
    }
    ambi.Inserte(datos)
    id=0
    msgitos = "Ambiente de formación creado"
    return render_template("alertas.html", msgito=msgitos)


#ADD WORKSTATIONS TO A LEARNING CLASSROOM:
@ambientes.route("add/pts/i", methods = ["POST"])
@login_required
def add_wks():
    idAmbiente = request.form.get('idAmbiente')
    idPuestoTrabajo = request.form.get('idPuestoTrabajo')
    ambi = Usuario("http://127.0.0.1:5000/ambientes/add/pts")
    datos = {
        "idAmbiente": idAmbiente,
        "idPuestoTrabajo": idPuestoTrabajo
    }
    ambi.Inserte(datos)
    id=0
    msgitos = "Puesto de trabajo asignado"
    return render_template("alertas.html", msgito=msgitos)


#ADD WKS TO A LEARNING CLASSROOM:
@ambientes.route("add/pts/<idAmbiente>", methods=["GET"])
@login_required
def AddElementsToAWorkstation(idAmbiente):
    response = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    puestos_t = response.json()

    ambi = requests.get(f"http://127.0.0.1:5000/ambientes/{idAmbiente}")
    learning_classrooms = ambi.json()
    print (f"Current leaning classroom: {learning_classrooms}")


    return render_template("ambientes.html", N=8, puestos_t=puestos_t,learning_classrooms=learning_classrooms)




#REGISTRO DE AMBIENTE DE FORMACION:
@ambientes.route("1", methods = ["GET","POST"])
@login_required
def ambiente_record():
    response = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    puestos_t = response.json()
    return render_template("ambientes.html", N='1', puestos_t=puestos_t)


#ACTUALIZA AMBIENTE:
@ambientes.route("u", methods=["POST"])
@login_required
def ActualizaAmbiente():
    id = request.form.get('id')
    idPuestoElemento=request.form.get('idPuestoElemento')
    nombreAmbiente=request.form.get('nombreAmbiente')
    ambi= Usuario("http://127.0.0.1:5000/ambientes")
    datos = {   
        "idAmbiente":id,
        "idPuestoElemento": idPuestoElemento,
        "nombreAmbiente": nombreAmbiente,
    }   
    ambi.Actualiza(datos)
    id=0
    msgitos = "Ambiente editado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

@ambientes.route("e/<id>", methods=["GET"])
@login_required
def EditaAmbiente(id):
    ambi= Usuario("http://127.0.0.1:5000/ambientes")
    pue_tra = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    puesto_t = pue_tra.json()
    nombre_ambi = ambi.ListarUno(id)
    return render_template("ambientes.html", N=2, puesto_t=puesto_t, nombre_ambi=nombre_ambi)


#DELETE LEARNING CLASSROOMS:
@ambientes.route("d/<id>", methods = ["GET"])
@login_required
def ambientesBorra(id):
    ambi = Usuario("http://127.0.0.1:5000/ambientes")
    cadena = ambi.Borra(id)
    msgitos = "Ambiente borrado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)



#LEARNING CLASSROOMS - LIST (accountant)
@ambientes.route("cuentadante", methods=["GET"])
@login_required
def ambientesCuentadante():
    idInstructor = current_user.idInstructor  # Assuming this attribute exists on your User class
    instructors_by_idAmbiente = requests.get(f"http://127.0.0.1:5000/instructores/ambientes/{idInstructor}")
    clss_by_an_instructor = instructors_by_idAmbiente.json()
    print(f"Learning classrooms that belong to an accountant: \n {clss_by_an_instructor}")

    classrooms = requests.get("http://127.0.0.1:5000/ambientes/to").json()

    # Extract the names of the classrooms associated with the instructor
    classroom_names = [classroom[1] for classroom in classrooms if classroom[0] in [ambie[1] for ambie in clss_by_an_instructor]]

    return render_template("lista_ambientes_cuentadante.html", clss_by_an_instructor=clss_by_an_instructor, classroom_names=classroom_names)