from flask import request
from flask import render_template

from flask_login import current_user

import requests
from services.apicnx import Usuario


from flask import Blueprint

elementos = Blueprint('elementos', __name__, url_prefix='/elementos',
                      template_folder='templates')


#NIVELES
@elementos.route("/0",methods=["GET","POST"])
def index():
    return render_template("niveles.html",N="0")

@elementos.route("/<id>",methods=["GET","POST"])
def nivel(id=0):
    return render_template("niveles.html",N=id)

    
#LEVEL LIST
@elementos.route("", methods=["GET"])
def ListarTodos():
    response = requests.get("http://127.0.0.1:5000/usua/tipo")
    tipo_elementos = response.json()

    ambientes_response = requests.get("http://127.0.0.1:5000/ambientes/add/pts")
    ambiente_puesto = ambientes_response.json()
    print(f"Ambiente Puesto: {ambiente_puesto}")

    instructor_pt_response = requests.get("http://127.0.0.1:5000/ambientes/pts")
    i = instructor_pt_response.json()
    print(f"Initial Workstations List (i): {i}")

    elements = requests.get("http://127.0.0.1:5000/puestos/trabajo/add/elements").json()

    idInstructor = current_user.idInstructor
    idTipoInstructor = current_user.idTipoInstructor

    arias = []
    cadena = []
    can = 0

    if idTipoInstructor == 1:
        instructors_by_idAmbiente_response = requests.get(f"http://127.0.0.1:5000/instructores/ambientes/{idInstructor}")
        clss_by_an_instructor = instructors_by_idAmbiente_response.json()
        print(f"Learning classrooms that belong to an accountant: \n{clss_by_an_instructor}")

        u1 = Usuario("http://127.0.0.1:5000/usua")
        cadena = list(u1.ListarTodos())
        can = len(cadena)

        ele = requests.get("http://127.0.0.1:5000/usua/to").json()

        # Loop through each classroom that belongs to the instructor
        for classroom in clss_by_an_instructor:
            idInstructor_classroom = classroom[0]  # idInstructor from the classroom list
            idAmbiente = classroom[1]  # idAmbiente from the classroom list

            # Check against each workstation
            for workstation in i:
                ws_idAmbiente = workstation[0]  # idAmbiente from the workstation list
                ws_idPuestoTrabajo = workstation[1]  # idPuestoTrabajo from the workstation list

                # Check if the workstation belongs to the current user's classroom
                if idAmbiente == ws_idAmbiente:
                    # Find the name of the puesto trabajo
                    ws_name = next((x[3] for x in ambiente_puesto if x[2] == ws_idPuestoTrabajo), None)

                    # Get elements for this workstation
                    for x in elements:
                        idPuestoTrabajo_element = x[0]
                        idElemento = x[1]

                        if idPuestoTrabajo_element == ws_idPuestoTrabajo:
                            # Get the name of the element
                            nombreElemento = next((e[2] for e in ele if e[0] == idElemento), None)
                            # Add the workstation and element details to the list
                            arias.append((idInstructor_classroom, ws_idPuestoTrabajo, ws_name, nombreElemento, idElemento))

                            for l in arias:
                                if l[4] not in ele:
                                    print ("No está.")
                                else:
                                    print ("Sí está, pero el elemento sí fue eliminado.")

                            

                    print(f"Workstation that belongs to {idInstructor_classroom}: {ws_name} \n These are the elements: {nombreElemento}")
                    print ("Data from arias variable",arias)


    elif idTipoInstructor == 3:
        u1 = Usuario("http://127.0.0.1:5000/usua")
        cadena = list(u1.ListarTodos())
        can = len(cadena)

    return render_template("niveles.html", N=0, tipo_elementos=tipo_elementos, cadena=cadena, can=can, arias=arias)




#NEW ELEMENT:
@elementos.route("i", methods=["POST"])
def nivelInserta():
    idTipoElemento = request.form.get('idTipoElemento')
    nombreElemento = request.form.get('nombreElemento')
    barcode = request.form.get('barcode')
    u1 = Usuario("http://127.0.0.1:5000/usua")
    datos = {   
        "idTipoElemento": idTipoElemento,
        "nombreElemento": nombreElemento,
        "barcode": barcode,
    }
    u1.Inserte(datos)
    msgitos = "Elemento creado satisfactoriamente"

    idInstructor = current_user.idInstructor
    idTipoInstructor = current_user.idTipoInstructor
    if idTipoInstructor == 1:
        ListarTodos()
        msgitos = "Lo insertó un cuentadante"
    elif idTipoInstructor == 3:
        ListarTodos()
        msgitos = "Lo insertó un admin"
    return render_template("alertas.html", msgito=msgitos)




#ACTUALIZA ELEMENTO:
@elementos.route("u", methods=["POST"])
def nivelactualiza():
    id = request.form.get('id')
    idTipoElemento=request.form.get('idTipoElemento')
    nombreElemento=request.form.get('nombreElemento')
    barcode = request.form.get('barcode')
    u1= Usuario("http://127.0.0.1:5000/usua")
    datos = {   
        "idElemento":id,
        "idTipoElemento": idTipoElemento,
        "nombreElemento": nombreElemento,
        "barcode": barcode,
    }   
    u1.Actualiza(datos)
    id=0
    msgitos = "Elemento editado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

@elementos.route("e/<id>", methods=["GET"])
def nivelEdita(id):
    u1 = Usuario("http://127.0.0.1:5000/usua")
    response = requests.get("http://127.0.0.1:5000/usua/tipo")
    tipo_elementos = response.json()
    cadena = u1.ListarUno(id)
    return render_template("niveles.html", N=2, tipo_elementos=tipo_elementos, cadena=cadena)



#DELETE LEVELS: 
@elementos.route("d/<id>",methods=["GET"])
def nivelBorra(id):
    u1= Usuario("http://127.0.0.1:5000/usua")
    cadena=u1.Borra(id)
    msgitos="Elemento borrado satisfactoriamente"
    return render_template("alertas.html",msgito=msgitos)
