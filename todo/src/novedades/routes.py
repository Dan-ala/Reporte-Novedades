from flask import Flask, jsonify,request
from flask import render_template
from flask_login import current_user
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
    print("Data to insert:", datos)
    nove.Inserte(datos)

    msgitos = "Novedad General registrada"

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

    # Fetching classroom_name
    csss = requests.get(f"http://127.0.0.1:5000/papa/{idPuestoTrabajo}")
    csss.raise_for_status()  # Raise HTTPError for bad responses

    # Extracting the correct classroom_name from the JSON response
    classroom_data = csss.json()

    if isinstance(classroom_data, list) and len(classroom_data) > 0:
        # Assuming the first element in the list is always the matched classroom
        classroom_name = classroom_data[0][0]
    else:
        classroom_name = "Unknown"  # Handle case where classroom_name extraction fails

    print("Classroom Name:", classroom_name)

    msgitos = ""
    try:
        idAmbi_response = requests.get(f"http://127.0.0.1:5000/reporte/{idPuestoTrabajo}")
        idAmbi_response.raise_for_status()
        idAmbiente_data = idAmbi_response.json()
        if isinstance(idAmbiente_data, list) and len(idAmbiente_data) > 0 and isinstance(idAmbiente_data[0], list):
            idAmbiente = idAmbiente_data[0][0]
        else:
            idAmbiente = None

        if idAmbiente is None:
            return "Could not determine idAmbiente", 500

        #GETTING THE IDINSTRUCTOR
        idInst_response = requests.get(f"http://127.0.0.1:5000/reporte2/{idAmbiente}")
        idInst_response.raise_for_status()
        IdInstructor_data = idInst_response.json()
        if isinstance(IdInstructor_data, list) and len(IdInstructor_data) > 0 and isinstance(IdInstructor_data[0], list):
            IdInstructor = IdInstructor_data[0][0]
        else:   
            IdInstructor = None

        if IdInstructor is None:
            return "Could not determine IdInstructor", 500

        #GETTING THE EMAIL
        ema_response = requests.get(f"http://127.0.0.1:5000/reporte3/{IdInstructor}")
        ema_response.raise_for_status()
        accountant_email = ema_response.json()
        if isinstance(accountant_email, list) and len(accountant_email) > 0 and isinstance(accountant_email[0], list):
            email = accountant_email[0][0]
        else:
            email = None

        if email is None:
            return "Could not determine email", 500
            

        msgitos = "Novedad registrada pero no se encontró el profesor correspondiente para enviar el correo."

        if email:
            try:
                msg = Message(
                    "REPORTE DE NOVEDAD",
                    sender="davisanquevedovan@gmail.com",
                    recipients=[email]
                )

                msg.html = f"""
                <h3>AMBIENTE DE FORMACION: {classroom_name}</h3>
                <h3>PUESTO DE TRABAJO: {nombrePT}</h3>
                <h3>ELEMENTO: {nombreElemento}</h3>
                <p>DESCRIPCION: {descripcion_novedad}</p>

                <br>

                <h1>"Señor usuario recuerde que los servicios del SENA son gratuitos"<h1>
                
                <h3>
                    <img src="todo/src/app/static/images/CGMLTI.png" alt="CGMLTI" width="88px">
                    <b>davisanquevedovan@gmail.com</b>
                    PBX:+(57) 601 5461500 Ext:17003
                    <b>Calle 52 No 13-65</b>
                <h3>
                """
                mail.send(msg)
                msgitos = "Novedad registrada y correo enviado al profesor correspondiente."
            except Exception as e:
                print(f"Error sending email: {e}")
                msgitos = "Novedad registrada pero hubo un error al enviar el correo."
        else:
            print("No matching instructor found for the given classroom.")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"JSON decoding error: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return render_template("alertas.html", msgito=msgitos, idPuestoTrabajo=idPuestoTrabajo, idElemento=idElemento)






#GENERAL NOVELTY
@novedades.route("i2", methods=["GET","POST"])
def gn():
    idAmbiente = str(request.form.get('idAmbiente'))
    descripcion_novedad = request.form.get('descripcion_novedad')

    nove = Usuario("http://127.0.0.1:5000/novedades_generales")
    datos = {
        "idAmbiente": idAmbiente,
        "descripcion_novedad": descripcion_novedad
    }
    print("Data to insert:", datos)
    nove.Inserte(datos)
    msgitos = "Novedad General registrada"
    return render_template("alertas.html", msgito=msgitos, idAmbiente=idAmbiente)











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
    
    # Get the data from the endpoints
    novedades = requests.get("http://127.0.0.1:5000/novedades").json()
    id_puesto_trabajo = requests.get("http://127.0.0.1:5000/puestos/trabajo").json()
    id_elemento = requests.get("http://127.0.0.1:5000/usua/to").json()
    
    idPT_dict = {puesto[0]: puesto[1] for puesto in id_puesto_trabajo}
    idElemento_dict = {elemento[0]: elemento[2] for elemento in id_elemento}

    idInstructor = current_user.idInstructor
    idTipoInstructor = current_user.idTipoInstructor
    
    matching_workstations = []

    if idTipoInstructor == 1:
        instructors_by_idAmbiente_response = requests.get(f"http://127.0.0.1:5000/instructores/ambientes/{idInstructor}")
        clss_by_an_instructor = instructors_by_idAmbiente_response.json()

        ambientes_response = requests.get("http://127.0.0.1:5000/ambientes/add/pts")
        ambiente_puesto = ambientes_response.json()

        instructor_pt_response = requests.get("http://127.0.0.1:5000/ambientes/pts")
        i = instructor_pt_response.json()

        for classroom in clss_by_an_instructor:
            idInstructor_classroom = classroom[0]
            idAmbiente = classroom[1]

            for workstation in i:
                ws_idAmbiente = workstation[0]
                ws_idPuestoTrabajo = workstation[1]

                if idAmbiente == ws_idAmbiente:
                    ws_name = next((x[3] for x in ambiente_puesto if x[2] == ws_idPuestoTrabajo), None)

                    for novelty in novedades:
                        if novelty[1] == ws_idPuestoTrabajo:
                            novelty_elements = [elem[0] for elem in id_elemento if elem[0] == novelty[2]]
                            novelty_description = novelty[3]
                            novelty_date = novelty[4]
                            matching_workstations.append((ws_name, novelty_elements, novelty_description, novelty_date))

    elif idTipoInstructor == 3:
        for novelty in novedades:
            idPT = novelty[1]
            idElemento = novelty[2]
            description = novelty[3]
            date = novelty[4]
            matching_workstations.append((idPT, idElemento, description, date))

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_novedades = matching_workstations[start_idx:end_idx]

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'cadena': paginated_novedades,
            'idPT_dict': idPT_dict,
            'idElemento_dict': idElemento_dict,
            'can': len(matching_workstations)
        })
    
    return render_template("novedades.html", N=0, cadena=paginated_novedades, idPT_dict=idPT_dict, idElemento_dict=idElemento_dict, can=len(matching_workstations), current_page=page, rows_per_page=per_page)




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



# REGISTRO NOVEDAD GENERAL
@novedades.route("/registro/general/<idAmbiente>", methods=["GET"])
def NovedadGeneral(idAmbiente):
    try:
        # Default to 'Unknown Classroom' if no classroom_name is provided
        classroom_name = request.args.get('classroom_name', 'Unknown Classroom')
        print(f"Received ID Ambiente: {idAmbiente}")
        print(f"Classroom Name: {classroom_name}")

        # Fetching data and rendering template with the classroom_name
        return render_template("novedades.html", N=2, classroom_name=classroom_name, idAmbiente=idAmbiente)
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
