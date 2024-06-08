from flask import render_template

from flask import Blueprint

menu = Blueprint('menu', __name__, url_prefix='/menu',
                      template_folder='templates')

#INDEX PAGE:
@menu.route("", methods = ["GET"])
def Lista():
    menu = (["Ambientes","Instructores","Puesto de Trabajo","Novedades","Elementos"])
    menu1 = (["ambientes.jpg","instructores.jpeg","pt.png","novelties.png","elementos.jpg"])
    n = len(menu)
    menu=[[
        {
            "Title":"Ambientes",
            "icons":"ambientes.jpg",
            "link":"/ambientes"
        },
        {
            "Title":"Instructores",
            "icons":"instructores.jpeg",
            "link":"/instructores"
        },
        {
            "Title":"Puestos de Trabajo",
            "icons": "pt.png",
            "link": "/puesto_trabajo"
        },
        {
            "Title": "Novedades",
            "icons": "novelties.png",
            "link": "/novedades"
        },
        {
            "Title": "Elementos",
            "icons": "elementos.jpg",
            "link": "/elementos"
        },
    ]]
    return render_template("index.html", menu=menu)