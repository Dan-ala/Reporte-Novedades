
from flask import Flask, jsonify,request
import json

from database.cnxSqlite import cnxsqlite  
from config import configura 

from datetime import datetime
import pytz

app=Flask(__name__)

#LOGIN
@app.route("/instruc")
def login():
    sql = "SELECT cedula, emailInstructor FROM instructor" 
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)

@app.route("/instructor/<id>")
def instr(id):
    sql = "SELECT * FROM instructor WHERE idInstructor = "+str(id)
    con=cnxsqlite()
    todo=con.Consultar("./novedades.db",sql)
    return json.dumps(todo)

#LISTS:
@app.route("/usua/to")
def ListaUsuario():
    sql="select * from elemento" 
    con=cnxsqlite()
    todo=con.Consultar("./novedades.db",sql)
    return json.dumps(todo)

@app.route("/ambientes/to")
def ListOneLearningClassroom():
    sql="select * from ambiente" 
    con=cnxsqlite()
    todo=con.Consultar("./novedades.db",sql)
    return json.dumps(todo)

@app.route("/usua/to2")
def elements():
    sql="select idElemento, nombreElemento FROM elemento" 
    con=cnxsqlite()
    todo=con.Consultar("./novedades.db",sql)
    return json.dumps(todo)

@app.route("/ele/<id>")
def yg(id):
    sql="select * FROM elemento where idElemento ="+str(id) 
    con=cnxsqlite()
    todo=con.Consultar("./novedades.db",sql)
    return json.dumps(todo)

@app.route("/usua/tipo")
def ListaTipoElemento():
    sql = "select * from tipo_elemento" 
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)

@app.route("/tipo/instructor")
def TipoInstructor():
    sql = "SELECT * FROM tipo_instructor"
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)

@app.route("/puestos/trabajo")
def ListaPuestosTrabajo():
    sql = "SELECT * from puesto_trabajo" 
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)

@app.route("/puestos/trabajo/add/elements")
def ss():
    sql = "SELECT * from puesto_elemento"
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)

@app.route("/ambientes/add/pts")
def qrs():
    sql = """
    SELECT ap.idAmbiente, a.nombreAmbiente, ap.idPuestoTrabajo, pt.nombrePT
    FROM ambiente_puesto ap
    JOIN ambiente a ON ap.idAmbiente = a.idAmbiente
    JOIN puesto_trabajo pt ON ap.idPuestoTrabajo = pt.idPuestoTrabajo
    """
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)  


#test
@app.route("/papa/<id>")
def papa(id):
    sql = """
    SELECT a.nombreAmbiente
        FROM ambiente_puesto ap
        INNER JOIN ambiente a ON ap.idAmbiente = a.idAmbiente
        WHERE ap.idPuestoTrabajo = 
    """+str(id)
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)

@app.route("/reporte/<id>")
def reporte1(id):
    sql = """
    SELECT idAmbiente
    FROM ambiente_puesto
    WHERE idPuestoTrabajo = 
    """+str(id)
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo) 

@app.route("/reporte2/<id>")
def report(id):
    sql = """
    SELECT idInstructor
    FROM instructor_ambientes
    WHERE idAmbiente =
    """+str(id)
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)

@app.route("/reporte3/<id>") 
def reports(id):
    sql = """
    SELECT emailInstructor 
    FROM instructor 
    WHERE idInstructor =
    """+str(id)+" AND idTipoInstructor = 1"
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)


@app.route("/ambientes/pts")
def ambi_pts():
    sql = "SELECT * FROM ambiente_puesto"
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)


@app.route("/puestos/trabajo/<id>")
def pepe(id):
    sql="select * from puesto_trabajo where idPuestoTrabajo="+str(id)
    con=cnxsqlite()
    todo=con.Consultar("./novedades.db",sql)
    return json.dumps(todo)

@app.route("/instructores")
def ListaInstructores():
    sql = "SELECT * FROM instructor" 
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)


#LISTAR INSTRUCTOR_AMBIENTES
@app.route("/instructores/ambientes")
def ListarInsAmbientes():
    sql = "SELECT * FROM instructor_ambientes"
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db",sql)
    return json.dumps(todo)


@app.route("/instructores/ambientes/<id>")
def ListarInsPorAmbientes(id):
    sql = "SELECT * FROM instructor_ambientes WHERE idInstructor ="+str(id)
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db",sql)
    return json.dumps(todo)



@app.route("/novedades")
def ListaNovedades():
    sql = "SELECT * FROM novedades" 
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)

@app.route("/ambientes")
def ListaAmbiente():
    sql = "SELECT * FROM ambiente" 
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)

@app.route("/ambientes/<id>")
def ListaUnAmbiente(id):
    sql = "SELECT * FROM ambiente where idAmbiente=" + str(id) 
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)


@app.route("/usua/<id>")
def ListaUnUsuario(id):
    sql="select * from elemento where idElemento="+str(id)
    con=cnxsqlite()
    todo=con.Consultar("./novedades.db",sql)
    return json.dumps(todo)


@app.route("/pt/<id>")
def ListaUnPT(id):
    sql = "SELECT e.idElemento, e.nombreElemento, e.barcode FROM puesto_trabajo p INNER JOIN puesto_elemento pe ON p.idPuestoTrabajo = pe.idPuestoTrabajo INNER JOIN elemento e ON pe.idElemento = e.idElemento WHERE p.idPuestoTrabajo =" + str(id)
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
    return json.dumps(todo)



@app.route("/pt/i", methods=['POST'])
def insert_general_novelty():
    datos = request.get_json()
    idPuestoTrabajo = datos['idPuestoTrabajo']
    descripcion_novedad = datos['descripcion_novedad']
    sql = "INSERT INTO novedades (idPuestoTrabajo,descripcion_novedad) VALUES ('"+idPuestoTrabajo+"','"+descripcion_novedad+"')"
    con = cnxsqlite()
    todo=con.Ejecutar("./novedades.db",sql)
    return "OK"

def get_local_time():
    utc_now = datetime.utcnow()
    local_tz = pytz.timezone('America/Bogota')
    local_time = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

@app.route("/novedades/i", methods=['POST'])
def insert_element_novelty():   
    datos = request.get_json()
    idPuestoTrabajo = datos['idPuestoTrabajo']
    idElemento = datos['idElemento']
    descripcion_novedad = datos['descripcion_novedad']
    date_novedad = get_local_time()
    sql = "INSERT INTO novedades (idPuestoTrabajo, idElemento, descripcion_novedad, date_novedad) VALUES ('"+idPuestoTrabajo+"','"+idElemento+"','"+descripcion_novedad+"','"+date_novedad+"')"
    con = cnxsqlite()
    todo=con.Ejecutar("./novedades.db",sql)
    return "OK"





















@app.route("/usua/i", methods=['POST'])
def CrearUsuario(): 
    datos = request.get_json()
    idTipoElemento = datos['idTipoElemento']
    nombreElemento = datos['nombreElemento']
    barcode = datos['barcode']

    sql = "INSERT INTO elemento (idTipoElemento, nombreElemento, barcode) VALUES ('"+idTipoElemento+"','"+nombreElemento+"','"+barcode+"')"
    con = cnxsqlite()
    todo=con.Ejecutar("./novedades.db",sql)
    return "OK" 

#NEW LEARNING CLASSROOM:
@app.route("/ambientes/i", methods=["POST"])
def CrearAmbiente():
    datos = request.get_json()
    nombreAmbiente = datos['nombreAmbiente']
    sql = "INSERT INTO ambiente (nombreAmbiente) VALUES ('"+nombreAmbiente+"')"
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "OK"

@app.route("/instructores/i", methods = ["POST"])
def CrearInstructor():
    datos = request.get_json()
    idTipoInstructor = datos['idTipoInstructor']
    cedula = datos['cedula']
    emailInstructor = datos['emailInstructor']
    sql = "INSERT INTO instructor (idTipoInstructor, cedula, emailInstructor) VALUES ('"+idTipoInstructor+"','"+cedula+"','"+emailInstructor+"')"
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "OK"


#NEW WORKSTATION:
@app.route("/puesto_trabajo/i", methods = ["POST"])
def CrearPuestoTrabajo():
    datos = request.get_json()
    nombrePT = datos['nombrePT']
    sql = "INSERT INTO puesto_trabajo (nombrePT) VALUES ('"+nombrePT+"')"
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "OK"

#ADD ELEMENTS TO A WORKSTATION:
@app.route("/puestos/trabajo/add/elements/i", methods = ["POST"])
def AddElementsToAPWS():
    datos = request.get_json()
    idPuestoTrabajo = datos['idPuestoTrabajo']
    idElemento = datos['idElemento']
    sql = "INSERT INTO puesto_elemento (idPuestoTrabajo, idElemento) VALUES ('"+idPuestoTrabajo+"','"+idElemento+"')"
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "OK"


#ADD WORKSTATIONS TO A LEARNING CLASSROOM:
@app.route("/ambientes/add/pts/i", methods = ["POST"])
def AddWorkstationLearningClassrooms():
    datos = request.get_json()
    idAmbiente = datos['idAmbiente']
    idPuestoTrabajo = datos['idPuestoTrabajo']
    sql = "INSERT INTO ambiente_puesto (idAmbiente, idPuestoTrabajo) VALUES ('"+idAmbiente+"','"+idPuestoTrabajo+"')"
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "OK"    



#ADD WORKSTATIONS TO A LEARNING CLASSROOM:
@app.route("/instructores/add/learning/classrooms/i", methods = ["POST"])
def AddClssToAnInstructor():
    datos = request.get_json()
    idInstructor = datos['idInstructor']
    idAmbiente = datos['idAmbiente']
    sql = "INSERT INTO instructor_ambientes (idInstructor, idAmbiente) VALUES ('"+idInstructor+"','"+idAmbiente+"')"
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "OK"  



#EDITA ELEMENTO:
@app.route("/usua/u",methods = ['PUT'])
def EditaElemento(): 
    datos = request.get_json()
    id = datos['idElemento']    
    idTipoElemento = datos['idTipoElemento']
    nombreElemento = datos['nombreElemento']
    barcode = datos['barcode']
    
    sql = "UPDATE elemento SET nombreElemento = '" + str(nombreElemento) + "', barcode = '" + str(barcode) + "', idTipoElemento = '" + str(idTipoElemento) + "' WHERE idElemento = " + str(id)
    try:
        con = cnxsqlite()
        todo = con.Ejecutar("./novedades.db", sql)
        return "OK"
    except Exception as e:
        print("An error occurred:", str(e))
        return "Error: Internal Server Error"

#EDITA AMBIENTE:
@app.route("/ambientes/u",methods = ['PUT'])
def EditaAmbiente(): 
    datos = request.get_json()
    id = datos['idAmbiente']    
    nombreAmbiente = datos['nombreAmbiente']
    
    sql = "UPDATE ambiente SET nombreAmbiente = '" + str(nombreAmbiente) + "' WHERE idAmbiente = " + str(id)
    try:
        con = cnxsqlite()
        todo = con.Ejecutar("./novedades.db", sql)
        return "OK"
    except Exception as e:
        print("An error occurred:", str(e))
        return "Error: Internal Server Error"
    
#EDITA INSTRUCTORES:
@app.route("/instructores/u",methods = ['PUT'])
def EditaInstructor():
    datos = request.get_json()
    id = datos['idInstructor']
    idTipoInstructor = datos['idTipoInstructor']
    cedula = datos['cedula']
    emailInstructor = datos['emailInstructor']
    sql = "UPDATE instructor SET emailInstructor = '"+emailInstructor+"', idTipoInstructor = '"+idTipoInstructor+"', cedula = '"+cedula+"' WHERE idInstructor = "+str(id)
    try:
        con = cnxsqlite()
        todo = con.Ejecutar("./novedades.db",sql)
        return "OK"
    except Exception as e:
        print("An error occurred:", str(e))
        return "Error: Internal Server Error"
    
#EDITA PUESTO DE TRABAJO:
@app.route("/puesto_trabajo/u", methods = ['PUT'])
def EditaPT():
    datos = request.get_json()
    id = datos['idPuestoTrabajo']
    nombrePT = datos['nombrePT']
    sql = "UPDATE puesto_trabajo SET nombrePT = '"+nombrePT+"' WHERE idPuestoTrabajo = "+str(id)
    try:
        con = cnxsqlite()
        todo = con.Ejecutar("./novedades.db", sql)
        return "OK"
    except Exception as e:
        print("An error occurred:", str(e))
        return "Error: Internal Server Error"


#DELETE LEVEL
@app.route("/usua/d/<id>",methods = ['DELETE'])
def BorrarUsuario(id): 
    sql="delete from elemento where idElemento="+str(id)
    con=cnxsqlite()
    todo=con.Ejecutar("./novedades.db",sql)
    return "OK"

#DELETE WHOLE NOVELTIES
@app.route("/usua/d", methods = ['DELETE'])
def borrar_todas_las_novedades():
    sql = "DELETE FROM novedades"
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "YOU'VE DELETED ALL THE RECORDS"

#DELETE LEARNING CLASSROOM:
@app.route("/ambientes/d/<id>", methods = ['DELETE'])
def DeleteLearningClassroom(id):
    sql = "DELETE FROM ambiente WHERE idAmbiente ="+str(id)
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "WELL DONE"

#DELETE INSTRUCTOR:
@app.route("/instructores/d/<id>", methods = ['DELETE'])
def DeleteInstructor(id):
    sql = "DELETE FROM instructor WHERE idInstructor ="+str(id)
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "OKAY"

@app.route("/puesto_trabajo/d/<id>", methods = ['DELETE'])
def DeleteWorkstation(id):
    sql = "DELETE FROM puesto_trabajo WHERE idPuestoTrabajo ="+str(id)
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "GREAT"




if __name__=='__main__':
    app.run(debug=True,port=configura['PUERTOREST'],host='0.0.0.0')