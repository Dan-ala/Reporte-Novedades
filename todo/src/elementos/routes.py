from flask import request, redirect
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
@elementos.route("",methods=["GET"])
def ListarTodos():
    u1= Usuario("http://127.0.0.1:5000/usua")
    response = requests.get("http://127.0.0.1:5000/usua/tipo")
    tipo_elementos = response.json()
    cadena = list(u1.ListarTodos())
    can=len(cadena)
    id=0
    return render_template("niveles.html",N=0,tipo_elementos=tipo_elementos,cadena=cadena,can=can)




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
        "barcode": barcode
    }
    u1.Inserte(datos)
    # msgitos = "Elemento creado satisfactoriamente"
    return redirect('/elementos')




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
