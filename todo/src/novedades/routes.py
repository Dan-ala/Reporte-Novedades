from flask import Flask, jsonify, redirect,request,session,flash, url_for
from flask import render_template
import requests
from services.apicnx import Usuario


from flask_mail import Mail, Message

mail = Mail()


from flask import Blueprint

novedades = Blueprint('novedades', __name__, url_prefix='/novedades',
                      template_folder='templates')




#NEW NOVELTY:
@novedades.route("i", methods=["GET", "POST"])
def new_novelty():
    idPuestoTrabajo = str(request.form.get('idPuestoTrabajo'))
    idElemento = str(request.form.get('idElemento'))
    descripcion_novedad = request.form.get('descripcion_novedad')

    nove = Usuario("http://127.0.0.1:5000/novedades")
    datos = {
        "idPuestoTrabajo": idPuestoTrabajo,
        "idElemento": idElemento,
        "descripcion_novedad": descripcion_novedad
    }
    print("Datos to insert:", datos)
    nove.Inserte(datos)

    # Fetching data from APIs
    instructors = requests.get("http://127.0.0.1:5000/instructores").json()
    print("Instructors:", instructors)

    classrooms = requests.get("http://127.0.0.1:5000/ambientes/to").json()
    print("Classrooms:", classrooms)

    workstations = requests.get("http://127.0.0.1:5000/puestos/trabajo").json()
    print("Workstations:", workstations)

    elements = requests.get("http://127.0.0.1:5000/usua/to").json()
    print("Elements:", elements)

    inst_ambi = requests.get("http://127.0.0.1:5000/instructores/ambientes").json()
    print("Instructor-Ambiente Relationships:", inst_ambi)

    # Get nombrePT for the given idPuestoTrabajo
    nombrePT = next((pt[1] for pt in workstations if pt[0] == int(idPuestoTrabajo)), None)
    print("Nombre PT:", nombrePT)

    # Get nombreElemento for the given idElemento
    nombreElemento = next((e[2] for e in elements if e[0] == int(idElemento)), None)
    print("Nombre Elemento:", nombreElemento)

    # Get classroom_name for the given idPuestoTrabajo
    classroom_name = next((classroom[1] for classroom in classrooms if classroom[0] == int(idPuestoTrabajo)), None)
    print("Classroom Name:", classroom_name)

    # Find the instructor email using the environment id
    idAmbiente = next((ambi[1] for ambi in inst_ambi if ambi[0] == int(idPuestoTrabajo)), None)
    instructor_email = next((instructor[3] for instructor in instructors if instructor[0] == idAmbiente or instructor[0] != idAmbiente), None)
    print("Instructor Email:", instructor_email)

    msgitos = "Novedad registrada pero no se encontró el profesor correspondiente para enviar el correo."

    if instructor_email:
        try:
            msg = Message(
                "NUEVA NOVEDAD",
                sender="davisanquevedovan@gmail.com",
                recipients=[instructor_email]
            )
            msg.body = f"EN EL AMBIENTE: {classroom_name} \n PUESTO DE TRABAJO: {nombrePT} \n ELEMENTO: {nombreElemento} \n DESCRIPCION: \n {descripcion_novedad}"
            mail.send(msg)
            msgitos = "Novedad registrada y correo enviado al profesor correspondiente."
        except Exception as e:
            print(f"Error sending email: {e}")
            msgitos = "Novedad registrada pero hubo un error al enviar el correo."
    else:
        print("No matching instructor found for the given classroom.")

    return render_template("alertas.html", msgito=msgitos, idPuestoTrabajo=idPuestoTrabajo, idElemento=idElemento)




#NOVEDADES
@novedades.route("/0", methods=["GET","POST"])
def index4():
    return render_template("novedades.html",N="0")

@novedades.route("/<id>", methods=["GET","POST"])
def novelties(id=0):
    return render_template("novedades.html",N=id)


#NOVELTY LIST:
@novedades.route("", methods=["GET"])
def NoveltyList():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    novedades = requests.get("http://127.0.0.1:5000/novedades").json()
    id_puesto_trabajo = requests.get("http://127.0.0.1:5000/puestos/trabajo").json()
    id_elemento = requests.get("http://127.0.0.1:5000/usua/to").json()
    
    idPT_dict = {puesto[0]: puesto[1] for puesto in id_puesto_trabajo}
    idElemento_dict = {elemento[0]: elemento[2] for elemento in id_elemento}

    # Calculate start and end indices for pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_novedades = novedades[start_idx:end_idx]

    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'cadena': paginated_novedades,
            'idPT_dict': idPT_dict,
            'idElemento_dict': idElemento_dict,
            'can': len(novedades)
        })
    
    return render_template("novedades.html", N=0, cadena=paginated_novedades, idPT_dict=idPT_dict, idElemento_dict=idElemento_dict, can=len(novedades), current_page=page, rows_per_page=per_page)


#REGISTRO DE NOVEDAD
@novedades.route("/registrar/novedad/<workstation_id>/<element_id>", methods=["GET"])
def registrar_2novedad(workstation_id, element_id):
    try:
        workstation_name = request.args.get('nombrePT', 'Unknown Workstation')
        element_name = request.args.get('nombreElemento', 'Unknown Element')

        return render_template(
            "novedades.html",
            N = '1',
            workstation_name=workstation_name,
            element_name=element_name,
            workstation_id=workstation_id,
            element_id=element_id
        )
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return "Error: Failed to retrieve data from the endpoint"
    

#DELETE ALL RECORDS FROM NOVELTUES TABLE
@novedades.route("/niveles/d", methods = ["GET"])
def BorraTodo():
    hola = Usuario("http://127.0.0.1:5000/usua")
    cadena = hola.BorraTodo()
    msgitos = "Novedades eliminadas exitosamente"
    return render_template("alertas.html", msgito=msgitos)
