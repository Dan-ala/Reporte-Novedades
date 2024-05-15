import sqlite3 as sql

def get_elemento_name_for_puesto_trabajo(puesto_trabajo_id):
    con = sql.connect("./novedades.db")
    cur = con.cursor()

    # SQL query to retrieve the name of the elemento associated with the puesto_trabajo
    query = """
    SELECT elemento.nombreElemento
    FROM elemento
    INNER JOIN puesto_trabajo ON elemento.idElemento = puesto_trabajo.idElemento
    WHERE puesto_trabajo.IdPuestoTrabajo = ?
    """

    # Execute the query with the provided puesto_trabajo_id
    cur.execute(query, (puesto_trabajo_id,))
    
    # Fetch the result
    result = cur.fetchone()
    
    # Close the connection
    con.close()

    # Return the name of the elemento
    return result[0] if result else None
