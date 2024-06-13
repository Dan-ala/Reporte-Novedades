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
    instructors = requests.get("http://127.0.0.1:5000/instructores")
    cadena = instructors.json()
    print("Instructors:", cadena)

    ambi = requests.get("http://127.0.0.1:5000/ambientes/to")
    cadena2 = ambi.json()
    print("Classrooms:", cadena2)

    puesto_t = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    pt = puesto_t.json()
    print("Workstations:", pt)

    elementos = requests.get("http://127.0.0.1:5000/usua/to")
    element = elementos.json()
    print("Elements:", element)

    # Get nombrePT for the given idPuestoTrabajo
    nombrePT = None
    for puesto in pt:
        if puesto[0] == int(idPuestoTrabajo):
            nombrePT = puesto[1]
            break
    print("Nombre PT:", nombrePT)

    # Get nombreElemento for the given idElemento
    nombreElemento = None
    for e in element:
        if e[0] == int(idElemento):
            nombreElemento = e[2]
            break
    print("Nombre Elemento:", nombreElemento)

    msgitos = "Novedad registrada pero no se encontró el profesor correspondiente para enviar el correo."

    # Find the correct classroom name
    classroom_name = None
    for classroom in cadena2:
        if classroom[0] == int(idPuestoTrabajo):
            classroom_name = classroom[1]
            break
    print("Classroom Name:", classroom_name)

    # Find the correct instructor email
    instructor_email = None
    for instructor in cadena:
        if instructor[2] == int(idPuestoTrabajo):
            instructor_email = instructor[4]
            break
    print("Instructor Email:", instructor_email)

    if instructor_email:
        try:
            msg = Message(
                "NUEVA NOVEDAD",
                sender="danielala2006@outlook.es",
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
