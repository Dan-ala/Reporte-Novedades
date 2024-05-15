from flask import Flask, jsonify,request
import json

from database.cnxSqlite import cnxsqlite  
from config import configura 

app=Flask(__name__)

#BELONGS?
@app.route("/check-in")
def x():    
    sql = """
    SELECT ambi.idPuestoTrabajo, pt.nombrePT 
    FROM puesto_trabajo pt 
    INNER JOIN ambiente ambi ON pt.idPuestoTrabajo = ambi.idPuestoTrabajo
    """
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return json.dumps(todo)

#LOGIN
@app.route("/instruc")
def login():
    sql = "SELECT cedula, emailInstructor FROM instructor" 
    con = cnxsqlite()
    todo = con.Consultar("./novedades.db", sql)
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
    sql = "SELECT e.idElemento, e.nombreElemento, e.barcode FROM puesto_trabajo p INNER JOIN puesto_elemento pe ON p.idPuestoTrabajo = pe.idPuestoTrabajo INNER JOIN elemento e ON pe.idElemento = e.idElemento WHERE p.idPuestoTrabajo = " + str(id)
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

@app.route("/novedades/i", methods=['POST'])
def insert_element_novelty():
    datos = request.get_json()
    idPuestoTrabajo = datos['idPuestoTrabajo']
    idElemento = datos['idElemento']
    descripcion_novedad = datos['descripcion_novedad']
    sql = "INSERT INTO novedades (idPuestoTrabajo, idElemento, descripcion_novedad) VALUES ('"+str(idPuestoTrabajo)+"','"+str(idElemento)+"','"+str(descripcion_novedad)+"')"
    con = cnxsqlite()
    todo=con.Ejecutar("./novedades.db",sql)
    return "OK" 

@app.route("/pt/historial", methods=['GET'])
def get_novelties_report():
    sql = "SELECT * FROM novedades"
    con = cnxsqlite()
    todo=con.Consultar("./novedades.db",sql)
    return "GREAT"























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
    idPuestoTrabajo = datos['idPuestoTrabajo']
    nombreAmbiente = datos['nombreAmbiente']
    sql = "INSERT INTO ambiente (idPuestoTrabajo, nombreAmbiente) VALUES ('"+idPuestoTrabajo+"','"+nombreAmbiente+"')"
    con = cnxsqlite()
    todo = con.Ejecutar("./novedades.db", sql)
    return "OK"

@app.route("/instructores/i", methods = ["POST"])
def CrearInstructor():
    datos = request.get_json()
    idTipoInstructor = datos['idTipoInstructor']
    idAmbiente = datos['idAmbiente']
    cedula = datos['cedula']
    emailInstructor = datos['emailInstructor']
    sql = "INSERT INTO instructor (idTipoInstructor, idAmbiente, cedula, emailInstructor) VALUES ('"+idTipoInstructor+"','"+idAmbiente+"','"+cedula+"','"+emailInstructor+"')"
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
    idPuestoTrabajo = datos['idPuestoTrabajo']
    nombreAmbiente = datos['nombreAmbiente']
    
    sql = "UPDATE ambiente SET nombreAmbiente = '" + str(nombreAmbiente) + "', idPuestoTrabajo = '" + str(idPuestoTrabajo) + "' WHERE idAmbiente = " + str(id)
    try:
        con = cnxsqlite()
        todo = con.Ejecutar("./novedades.db", sql)
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