from json import decoder
from flask import Flask, redirect,request,session,flash, url_for
from flask import render_template
import requests
from services.apicnx import Usuario
from config import configura     
  
app=Flask(__name__)

app.secret_key = 'your_secret_key'

#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        r = requests.get("http://127.0.0.1:5000/instructores")
        cedula = int(request.form.get("cedula"))
        emailInstructor = request.form.get("emailInstructor")
        rs = r.json()
        print (rs)

        found = False
        for x in rs:
            if cedula == x[3] and emailInstructor == x[4] and x[1] == 1:
                session["cedula"] = cedula
                session["emailInstructor"] = emailInstructor
                found = True
                break
            elif cedula == x[3] and emailInstructor == x[4] and x[1] == 2:
                flash(f"El instructor con cc: {x[3]} NO es un cuentadante.")
                return redirect(url_for('login'))
        if found:
            return redirect("/menu")
        else:
            flash("Cédula o E-mail incorrectos")
            return redirect(url_for('login'))
        
    return render_template("login.html", error=error)



#INDEX PAGE:
@app.route("/menu", methods = ["GET"])
def Lista():
    menu = (["Ambientes","Instructores","Puesto de Trabajo","Novedades","Elementos"])
    menu1 = (["ambientes.jpg","instructores.jpeg","pt.png","novelties.png","elementos.jpg"])
    n = len(menu)
    menu=[[
        {
            "Title":"Ambientes",
            "icons":"ambientes.jpg",
            "link":"/ambientes/l"
        },
        {
            "Title":"Instructores",
            "icons":"instructores.jpeg",
            "link":"/instructores/l"
        },
        {
            "Title":"Puestos",
            "icons": "pt.png",
            "link": "/puesto_trabajo/l"
        },
        {
            "Title": "Novelties",
            "icons": "novelties.png",
            "link": "/novedades/l"
        },
        {
            "Title": "Elementos",
            "icons": "elementos.jpg",
            "link": "/niveles/l"
        },
    ]]
    return render_template("index.html", menu=menu)

#NIVELES
@app.route("/niveles/0",methods=["GET","POST"])
def index():
    return render_template("niveles.html",N="0")

@app.route("/niveles/<id>",methods=["GET","POST"])
def nivel(id=0):
    return render_template("niveles.html",N=id)

#PUESTO_TRABAJO
@app.route("/puesto_trabajo/0",methods=["GET","POST"])
def index2():
    return render_template("./pt/pt.html",N="0")

@app.route("/puesto_trabajo/<id>", methods=["GET","POST"])
def pt(id=0):
    return render_template("./pt/pt.html",N=id)

#INSTRUCTORES
@app.route("/instructores/0",methods=["GET","POST"])
def index3():
    return render_template("./instructores/instructores.html",N="0")

@app.route("/instructores/<id>", methods=["GET","POST"])
def instructores(id=0):
    return render_template("./instructores/instructores.html",N=id)

#NOVEDADES
@app.route("/novedades/0", methods=["GET","POST"])
def index4():
    return render_template("./novedades/novedades.html",N="0")

@app.route("/novedades/<id>", methods=["GET","POST"])
def novelties(id=0):
    return render_template("./novedades/novedades.html",N=id)

#AMBIENTES
@app.route("/ambientes/0", methods=["GET","POST"])
def index5():
    return render_template("./ambientes/ambientes.html", N="0")

@app.route("/ambientes/<id>", methods=["GET","POST"])
def learning_classroom(id=0):
    return render_template("./ambientes/ambientes.html", N=id)

#52
@app.route("/puestos/trabajo/add/elements/0", methods = ["GET","POST"])
def index6():
    return render_template("./pt/pt.html", N="0")

@app.route("/puestos/trabajo/add/elements/<id>", methods=["GET","POST"])
def l(id=0):
    return render_template("./pt/pt.html", N=id)
    
#NEW ELEMENT:
@app.route("/niveles/i", methods=["POST"])
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
    id=0
    msgitos = "Elemento creado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

#NEW LEARNING CLASSROOM
@app.route("/ambientes/i", methods=["POST"])
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

#NEW INSTRUCTOR
@app.route("/instructores/i",methods = ["POST"])
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

#NEW WORKSTATION
@app.route("/puesto_trabajo/i", methods = ["POST"])
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
@app.route("/puestos/trabajo/add/elements/i", methods = ["POST"])
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


#NEW NOVELTY:
@app.route("/novedades/i", methods=["POST"])
def new_novelty():
    idPuestoTrabajo = request.form.get('idPuestoTrabajo')
    idElemento = request.form.get('idElemento')
    descripcion_novedad = request.form.get('descripcion_novedad')
    print(f"idPuestoTrabajo: {idPuestoTrabajo}")
    print(f"idElemento: {idElemento}")
    print(f"descripcion_novedad: {descripcion_novedad}")

    nove= Usuario("http://127.0.0.1:5000/novedades")
    datos = {
        "idPuestoTrabajo":idPuestoTrabajo,
        "idElemento": idElemento,
        "descripcion_novedad": descripcion_novedad
    }
    # Debug print before insertion
    print("Datos to insert:", datos)
    nove.Inserte(datos)
    id=0
    msgitos = "Novedad registrada"
    return render_template("alertas.html", msgito=msgitos,idPuestoTrabajo=idPuestoTrabajo, idElemento=idElemento)

#REGISTRO DE NOVEDAD
@app.route("/novedades/registrar/novedad/<workstation_id>/<element_id>", methods=["GET"])
def registrar_2novedad(workstation_id, element_id):
    try:
        workstation_name = request.args.get('nombrePT', 'Unknown Workstation')
        element_name = request.args.get('nombreElemento', 'Unknown Element')

        return render_template(
            "./novedades/novedades.html",
            N = '1',
            workstation_name=workstation_name,
            element_name=element_name,
            workstation_id=workstation_id,
            element_id=element_id
        )
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return "Error: Failed to retrieve data from the endpoint"

#ADD ELEMENTS TO A WORKSTATION
@app.route("/ptrabajo/add/elements/<idPuestoTrabajo>", methods = ["GET"])
def AddElementsToAWorkstation(idPuestoTrabajo):
    puesto_trabajo = requests.get("http://127.0.0.1:5000/puestos/trabajo/"+idPuestoTrabajo)
    ele = requests.get("http://127.0.0.1:5000/usua/to")
    elements = ele.json()
    pts = puesto_trabajo.json()
    print(f"PTs: \n {pts}")
    print (f"Elements to add: \n {elements}")
    return render_template("./pt/pt.html", N=8, pts=pts, elements=elements)


#ACTUALIZA ELEMENTO:
@app.route("/niveles/u", methods=["POST"])
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

@app.route("/niveles/e/<id>", methods=["GET"])
def nivelEdita(id):
    u1 = Usuario("http://127.0.0.1:5000/usua")
    response = requests.get("http://127.0.0.1:5000/usua/tipo")
    tipo_elementos = response.json()
    cadena = u1.ListarUno(id)
    return render_template("niveles.html", N=2, tipo_elementos=tipo_elementos, cadena=cadena)

#ACTUALIZA AMBIENTE:
@app.route("/ambientes/u", methods=["POST"])
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

@app.route("/ambientes/e/<id>", methods=["GET"])
def EditaAmbiente(id):
    ambi= Usuario("http://127.0.0.1:5000/ambientes")
    pue_tra = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    puesto_t = pue_tra.json()
    nombre_ambi = ambi.ListarUno(id)
    return render_template("./ambientes/ambientes.html", N=2, puesto_t=puesto_t, nombre_ambi=nombre_ambi)

#ACTUALIZA INSTRUCTOR:
@app.route("/instructores/u", methods=["POST"])
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

@app.route("/instructores/e/<id>", methods=["GET"])
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

    return render_template("./instructores/instructores.html", N=2, inst=inst, tipo_inst=tipo_inst, cadena2=cadena2)

#ACTUALIZA PT:
@app.route("/puesto_trabajo/u", methods = ["POST"])
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

@app.route("/puesto_trabajo/e/<id>", methods = ["GET"])
def EditaPT(id):
    workstation = requests.get("http://127.0.0.1:5000/puestos/trabajo/" + id)
    one_workstation = workstation.json()
    print (one_workstation)
    return render_template("./pt/pt.html", N=2, one_workstation=one_workstation)


#PT
@app.route("/puesto_trabajo/pt/<id>", methods=["GET"])
def lulo(id):
    response = requests.get("http://127.0.0.1:5000/pt/" + id)
    r = requests.get("http://127.0.0.1:5000/puestos/trabajo/" + id)
    workstation = r.json()
    print(f"This is your workstation: \n {workstation}")

    if response.status_code == 200:
        elements = response.json()
        print(f"ELEMENTS: \n {elements}")
        cadena_dict = {item[0]: item[1] for item in elements}
        workstation_name = workstation[0][1] if workstation else "Unknown Workstation"
        return render_template(
            "./pt/pt.html", 
            N=0, 
            can=len(elements), 
            cadena=elements, 
            cadena_dict=cadena_dict, 
            workstation_id=id, 
            workstation_name=workstation_name
        )
    else:
        return "Error: Failed to retrieve data from the endpoint"

#DELETE LEVELS: 
@app.route("/niveles/d/<id>",methods=["GET"])
def nivelBorra(id):
    u1= Usuario("http://127.0.0.1:5000/usua")
    cadena=u1.Borra(id)
    msgitos="Elemento borrado satisfactoriamente"
    return render_template("alertas.html",msgito=msgitos)

#DELETE ALL RECORDS FROM NOVELTUES TABLE
@app.route("/niveles/d", methods = ["GET"])
def BorraTodo():
    hola = Usuario("http://127.0.0.1:5000/usua")
    cadena = hola.BorraTodo()
    msgitos = "Novedades eliminadas exitosamente"
    return render_template("alertas.html", msgito=msgitos)

#DELETE LEARNING CLASSROOMS:
@app.route("/ambientes/d/<id>", methods = ["GET"])
def ambientesBorra(id):
    ambi = Usuario("http://127.0.0.1:5000/ambientes")
    cadena = ambi.Borra(id)
    msgitos = "Ambiente borrado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

#DELETE INSTRUCTORS:
@app.route("/instructores/d/<id>", methods = ["GET"])
def instructoresBorra(id):
    instructores = Usuario("http://127.0.0.1:5000/instructores")
    cadena = instructores.Borra(id)
    msgitos = "Instructor borrado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

#DELETE WORKSTATIONS:
@app.route("/puesto_trabajo/d/<id>", methods = ["GET"])
def puestosTrabajoBorra(id):
    pts = Usuario("http://127.0.0.1:5000/puesto_trabajo")
    cadena = pts.Borra(id)
    msgitos = "Puesto de Trabajo borrado satisfactoriamente"
    return render_template("alertas.html", msgito=msgitos)

#LEVEL LIST
@app.route("/niveles/l",methods=["GET"])
def ListarTodos():
    u1= Usuario("http://127.0.0.1:5000/usua")
    response = requests.get("http://127.0.0.1:5000/usua/tipo")
    tipo_elementos = response.json()
    cadena = list(u1.ListarTodos())
    can=len(cadena)
    id=0
    return render_template("niveles.html",N=0,tipo_elementos=tipo_elementos,cadena=cadena,can=can)

#DESKTOP LIST:
@app.route("/puesto_trabajo/l",methods=["GET"])
def DesktopList():
    desktops= requests.get("http://127.0.0.1:5000/puestos/trabajo")
    cadena = desktops.json()
    can=len(cadena)

    response = requests.get("http://127.0.0.1:5000/usua/to2")
    elementos = response.json()
    id=0
    return render_template("./pt/pt.html",N=7,cadena=cadena,can=can,elementos=elementos)

#INSTRUCTOR LIST:
@app.route("/instructores/l", methods=["GET"])
def InstructorList():
    instructors = requests.get("http://127.0.0.1:5000/instructores")
    ambi = requests.get("http://127.0.0.1:5000/ambientes/to")
    t_instructors = requests.get("http://127.0.0.1:5000/tipo/instructor")
    cadena = instructors.json()
    cadena2 = ambi.json()
    tipo_inst = t_instructors.json()
    # print (f" Instructors: {cadena} \n and Learning Classrooms: {cadena2} \n and type of instructors: {tipo_inst}")
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
    return render_template("./instructores/instructores.html", N=0, cadena=cadena,can=can,cadena2=cadena2,classrooms_not_designated=classrooms_not_designated,tipo_inst=tipo_inst,msg=msg)

#NOVELTY LIST:
@app.route("/novedades/l", methods=["GET"])
def NoveltyList():
    novedades = requests.get("http://127.0.0.1:5000/novedades")
    id_puesto_trabajo = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    id_elemento = requests.get("http://127.0.0.1:5000/usua/to")
    cadena = novedades.json()
    idPT = id_puesto_trabajo.json()
    idElemento = id_elemento.json()
    print ("LIST OF NOVELTIES: \n",cadena)
    print ("LIST OF WORKSTATIONS: \n",idPT)
    print ("LIST OF ELEMENTS: \n",idElemento)
    can = len(cadena)
    id=0
    # Assuming you have lists idPT and idElemento
    idPT_dict = {puesto[0]: puesto[1] for puesto in idPT}
    idElemento_dict = {elemento[0]: elemento[2] for elemento in idElemento} 
    return render_template("./novedades/novedades.html", N=0, cadena=cadena, idPT=idPT, idPT_dict=idPT_dict, idElemento=idElemento, idElemento_dict=idElemento_dict, can=can)

#LEARNIGN CLASSROOM LIST:
@app.route("/ambientes/l", methods=["GET"])
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

    return render_template("./ambientes/ambientes.html", N=0, cadena=cadena, puesto_t=workstations_not_in_classroom,msg=msg)

#REGISTRO DE ELEMENTO:
@app.route("/niveles/1", methods=["GET", "POST"])
def create_record():
    response = requests.get("http://127.0.0.1:5000/usua/tipo")
    tipo_elementos = response.json()

    return render_template("niveles.html", N='1', tipo_elementos=tipo_elementos)

#REGISTRO DE AMBIENTE DE FORMACION:
@app.route("/ambientes/1", methods = ["GET","POST"])
def ambiente_record():
    response = requests.get("http://127.0.0.1:5000/puestos/trabajo")
    puestos_t = response.json()
    return render_template("./ambientes/ambientes.html", N='1', puestos_t=puestos_t)

#REGISTRO DE PUESTO DE TRABAJO:
@app.route("/puesto_trabajo/1", methods = ["GET","POST"])
def pt_record():
    response = requests.get("http://127.0.0.1:5000/usua/to2")
    elementos = response.json()
    return render_template("./pt/pt.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=configura['PUERTOAPP'])
    