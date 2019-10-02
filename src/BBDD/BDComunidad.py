import sqlite3


#nombre,codigo
def insertDefault():
    bbdd = sqlite3.connect("Weather.db")
    bbdd.row_factory = sqlite3.Row
    cursor = bbdd.cursor()

    cursor.execute("INSERT INTO Comunidad VALUES ('Comunidad de Madrid','mad');")
    cursor.execute("INSERT INTO Comunidad VALUES ('La Rioja','rio');")
    cursor.execute("INSERT INTO Comunidad VALUES ('Canarias','coo');")
    cursor.execute("INSERT INTO Comunidad VALUES ('Comunitat Valenciana','val');")
    
    #confirmamos
    bbdd.commit()

def deteleContenido():
    bbdd = sqlite3.connect("Weather.db")
    bbdd.row_factory = sqlite3.Row
    cursor = bbdd.cursor()
                     
    #el codigo de provincia de mdrid es 28
    cursor.execute("delete from Comunidad;")
    bbdd.commit()

insertDefault()