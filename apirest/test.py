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

    INSERT INTO instructor (idTipoInstructor, idAmbiente, cedula, emailInstructor)
    VALUES (1, 1, 1021396143, "dsalarcon3@sena.edu.co");

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

    INSERT INTO elemento (idTipoElemento, nombreElemento, barcode)
    VALUES (1, "CPU", "01330132"),
           (2, "Mouse", "01234567"),
           (2, "Keyboard", "98765432");

    CREATE TABLE puesto_trabajo (
        idPuestoTrabajo INTEGER PRIMARY KEY,
        nombrePT TEXT NOT NULL
    );

    INSERT INTO puesto_trabajo (nombrePT)
    VALUES ("PT1"),
           ("PT2");


    CREATE TABLE puesto_elemento (
        idPuestoTrabajo INTEGER,
        idElemento INTEGER,
        FOREIGN KEY(idPuestoTrabajo) REFERENCES puesto_trabajo(idPuestoTrabajo),
        FOREIGN KEY(idElemento) REFERENCES elemento(idElemento),
        PRIMARY KEY (idPuestoTrabajo, idElemento)
    );


    INSERT INTO puesto_elemento (idPuestoTrabajo, idElemento)
    VALUES (1, 1),
           (2, 2),
           (2, 3);

    CREATE TABLE ambiente (
        idAmbiente INTEGER PRIMARY KEY,
        idPuestoTrabajo INTEGER NOT NULL,
        nombreAmbiente TEXT NOT NULL,
        FOREIGN KEY(idPuestoTrabajo) REFERENCES puesto_trabajo(idPuestoTrabajo)
    );

    INSERT INTO ambiente (idPuestoTrabajo, nombreAmbiente)
    VALUES (1, "AMBIENTE 412");
    

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
    """
    
    cur.executescript(create_statements)
    con.commit()
    con.close()

def insert_general_novelty(idPuestoTrabajo, descripcion_novedad):
    con = sql.connect("novedades.db")
    cur = con.cursor()
    cur.execute("INSERT INTO novedades (idPuestoTrabajo, descripcion_novedad) VALUES (?, ?)",
                (idPuestoTrabajo, descripcion_novedad,))
    con.commit()
    con.close()

def insert_element_novelty(idPuestoTrabajo, idElemento, descripcion_novedad):
    con = sql.connect("novedades.db")
    cur = con.cursor()
    cur.execute("INSERT INTO novedades (idPuestoTrabajo, idElemento, descripcion_novedad) VALUES (?, ?, ?)",
                (idPuestoTrabajo, idElemento, descripcion_novedad,))
    con.commit()
    con.close()

def get_novelties_report():
    con = sql.connect("novedades.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM novedades")
    novelties = cur.fetchall()
    con.close()
    return novelties

if __name__ == "__main__":
    createDB()
    
    # Insert a general novelty for the desktop
    insert_general_novelty(2,"General novelty for desktop")
    
    # Insert a novelty for a specific element
    insert_element_novelty(1, 1, "Novelty for CPU")

    # Retrieve the inserted novelties
    novelties = get_novelties_report()
    print("All Novelties:")
    for novelty in novelties:
        print("ID:", novelty[0])
        if novelty[2]:  # Check if the novelty is associated with an element
            print("Element ID:", novelty[2])
            print("Description:", novelty[3])
        else:
            print("General Desktop Novelty")
            print("Description:", novelty[3])
        print("Date:", novelty[4])
        print()
