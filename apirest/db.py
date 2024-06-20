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
           ("INSTRUCTOR"),
           ("ADMINISTRADOR");

    CREATE TABLE instructor (
        idInstructor INTEGER PRIMARY KEY,
        idTipoInstructor INTEGER NOT NULL,
        cedula INTEGER NOT NULL,
        emailInstructor TEXT NOT NULL,
        FOREIGN KEY(idTipoInstructor) REFERENCES tipo_instructor(idTipoInstructor)
    );

    INSERT INTO instructor (idTipoInstructor, cedula, emailInstructor)
    VALUES (3, 1025141238, "davids_quevedo@soy.sena.edu.co"),
    (3, 1003673047, "jstunjano7@soy.sena.edu.co"),
    (3, 1021396143, "dsalarcon@soy.sena.edu.co");


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
        nombreAmbiente TEXT NOT NULL
    );

    CREATE TABLE ambiente_puesto (
    idAmbiente INTEGER,
    idPuestoTrabajo INTEGER,
    FOREIGN KEY(idAmbiente) REFERENCES ambiente(idAmbiente),
    FOREIGN KEY(idPuestoTrabajo) REFERENCES puesto_trabajo(idPuestoTrabajo),
    PRIMARY KEY (idAmbiente, idPuestoTrabajo)
    );

    CREATE TABLE instructor_ambientes (
    idInstructor INTEGER,
    idAmbiente INTEGER,
    FOREIGN KEY(idInstructor) REFERENCES instructor(idInstructor),
    FOREIGN KEY(idAmbiente) REFERENCES ambiente(idAmbiente),
    PRIMARY KEY (idInstructor, idAmbiente)
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