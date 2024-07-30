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
    VALUES (1, 123, "davisanquevedovan@gmail.com"),
           (1, 456, "danielala14fi@gmail.com"),
           (2, 1034567890, "instructor1@example.com"),
           (2, 1045678901, "instructor2@example.com"),
           (3, 1025141238, "davids_quevedo@soy.sena.edu.co"),
           (3, 1021396143, "dsalarcon3@soy.sena.edu.co");

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
        created_by INTEGER NOT NULL,
        FOREIGN KEY(idTipoElemento) REFERENCES tipo_elemento(idTipoElemento)
    );

    INSERT INTO elemento (idTipoElemento, nombreElemento, barcode, created_by)
    VALUES (1, "Monitor", "123456", 1),
           (2, "Mouse", "789012", 1),
           (1, "Keyboard", "345678", 3);

    CREATE TABLE puesto_trabajo (
        idPuestoTrabajo INTEGER PRIMARY KEY,
        nombrePT TEXT NOT NULL
    );

    INSERT INTO puesto_trabajo (nombrePT)
    VALUES ("Desk1"),
           ("Desk2"),
           ("Desk3");

    CREATE TABLE puesto_elemento (
        idPuestoTrabajo INTEGER,
        idElemento INTEGER,
        FOREIGN KEY(idPuestoTrabajo) REFERENCES puesto_trabajo(idPuestoTrabajo),
        FOREIGN KEY(idElemento) REFERENCES elemento(idElemento),
        PRIMARY KEY (idPuestoTrabajo, idElemento)
    );

    INSERT INTO puesto_elemento (idPuestoTrabajo, idElemento)
    VALUES (1, 1),
           (1, 2),
           (2, 3);

    CREATE TABLE ambiente (
        idAmbiente INTEGER PRIMARY KEY,
        nombreAmbiente TEXT NOT NULL
    );

    INSERT INTO ambiente (nombreAmbiente)
    VALUES ("Office1"),
           ("Office2");

    CREATE TABLE ambiente_puesto (
        idAmbiente INTEGER,
        idPuestoTrabajo INTEGER,
        FOREIGN KEY(idAmbiente) REFERENCES ambiente(idAmbiente),
        FOREIGN KEY(idPuestoTrabajo) REFERENCES puesto_trabajo(idPuestoTrabajo),
        PRIMARY KEY (idAmbiente, idPuestoTrabajo)
    );

    INSERT INTO ambiente_puesto (idAmbiente, idPuestoTrabajo)
    VALUES (1, 1),
           (1, 2),
           (2, 3);

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

    CREATE TABLE novedades_generales (
        idNG INTEGER PRIMARY KEY,
        idAmbiente INTEGER,
        descripcion_novedad TEXT NOT NULL,
        date_novedad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(idAmbiente) REFERENCES ambiente(idAmbiente)
    );


    CREATE TRIGGER delete_puesto_elemento
    AFTER DELETE ON puesto_trabajo
    FOR EACH ROW
    BEGIN
        DELETE FROM puesto_elemento WHERE idPuestoTrabajo = OLD.idPuestoTrabajo;
    END;


    CREATE TRIGGER delete_inst_ambientes
    AFTER DELETE ON instructor
    FOR EACH ROW
    BEGIN
        DELETE FROM instructor_ambientes WHERE idInstructor = OLD.idInstructor;
    END;

    
    CREATE TRIGGER delete_ambiente_puesto
    AFTER DELETE ON puesto_trabajo
    FOR EACH ROW
    BEGIN
        DELETE FROM ambiente_puesto WHERE idPuestoTrabajo = OLD.idPuestoTrabajo;
    END;
    """
    
    cur.executescript(create_statements)
    con.commit()
    con.close()

if __name__ == "__main__":
    createDB()