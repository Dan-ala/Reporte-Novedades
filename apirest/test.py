import sqlite3 as sql
from datetime import datetime

def createDB():
    con = sql.connect("novedades.db")
    cur = con.cursor()
    
    create_statements = """
    CREATE TABLE tipo_instructor (
        idTipoInstructor INTEGER PRIMARY KEY,
        tipoInstructor TEXT NOT NULL
    );

    INSERT INTO tipo_instructor (tipoInstructor)
    VALUES ("CUENTADANTE"),
           ("INSTRUCTOR");

    CREATE TABLE instructor (
        idInstructor INTEGER PRIMARY KEY,
        idTipoInstructor INTEGER NOT NULL,
        idAmbiente INTEGER NOT NULL,
        cedula INTEGER NOT NULL,
        emailInstructor TEXT NOT NULL,
        FOREIGN KEY(idTipoInstructor) REFERENCES tipo_instructor(idTipoInstructor),
        FOREIGN KEY(idAmbiente) REFERENCES ambiente(idAmbiente)
    );



    CREATE TABLE tipo_elemento (
        idTipoElemento INTEGER PRIMARY KEY,
        tipo TEXT NOT NULL
    );

    INSERT INTO tipo_elemento (tipo)
    VALUES ("INVENTARIADO"),
           ("NO INVENTARIADO");

    CREATE TABLE elemento (
        idElemento INTEGER PRIMARY KEY,
        idTipoElemento INTEGER NOT NULL,
        nombreElemento TEXT NOT NULL,
        barcode TEXT NOT NULL,
        FOREIGN KEY(idTipoElemento) REFERENCES tipo_elemento(idTipoElemento)
    );



    CREATE TABLE puesto_trabajo (
        idPuestoTrabajo INTEGER PRIMARY KEY,
        nombrePT TEXT NOT NULL
    );




    CREATE TABLE puesto_elemento (
        idPuestoTrabajo INTEGER,
        idElemento INTEGER,
        FOREIGN KEY(idPuestoTrabajo) REFERENCES puesto_trabajo(idPuestoTrabajo),
        FOREIGN KEY(idElemento) REFERENCES elemento(idElemento),
        PRIMARY KEY (idPuestoTrabajo, idElemento)
    );




    CREATE TABLE ambiente (
        idAmbiente INTEGER PRIMARY KEY,
        idPuestoTrabajo INTEGER NOT NULL,
        nombreAmbiente TEXT NOT NULL,
        FOREIGN KEY(idPuestoTrabajo) REFERENCES puesto_trabajo(idPuestoTrabajo)
    );


    

    CREATE TABLE novedades (
        idNovedad INTEGER PRIMARY KEY,
        idPuestoTrabajo INTEGER,
        idElemento INTEGER,
        descripcion_novedad TEXT NOT NULL,
        date_novedad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(idPuestoTrabajo) REFERENCES puesto_trabajo(idPuestoTrabajo),
        FOREIGN KEY(idElemento) REFERENCES elemento(idElemento)
    );

    CREATE TABLE novedades_elementos (
        idNovedad INTEGER,
        idElemento INTEGER,
        FOREIGN KEY(idNovedad) REFERENCES novedades(idNovedad),
        FOREIGN KEY(idElemento) REFERENCES elemento(idElemento),
        PRIMARY KEY(idNovedad, idElemento)
    );

    
    
    CREATE TRIGGER delete_element_trigger
    AFTER DELETE ON elemento
    FOR EACH ROW
    BEGIN
        DELETE FROM puesto_elemento WHERE idElemento = OLD.idElemento;
    END;

    CREATE TRIGGER delete_workstation_trigger
    AFTER DELETE ON puesto_trabajo
    FOR EACH ROW
    BEGIN
        DELETE FROM puesto_elemento WHERE idPuestoTrabajo = OLD.idPuestoTrabajo;
    END;
    """
    
    cur.executescript(create_statements)
    con.commit()
    con.close()

if __name__ == "__main__":
    createDB()
    
    # # Insert a general novelty for the desktop
    # insert_general_novelty(2,"General novelty for desktop")
    
    # # Insert a novelty for a specific element
    # insert_element_novelty(1, 1, "Novelty for CPU")

    # # Retrieve the inserted novelties
    # novelties = get_novelties_report()
    # print("All Novelties:")
    # for novelty in novelties:
    #     print("ID:", novelty[0])
    #     if novelty[2]:  # Check if the novelty is associated with an element
    #         print("Element ID:", novelty[2])
    #         print("Description:", novelty[3])
    #     else:
    #         print("General Desktop Novelty")
    #         print("Description:", novelty[3])
    #     print("Date:", novelty[4])
    #     print()
