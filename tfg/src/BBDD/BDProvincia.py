import sqlite3

import sqlite3
import os

class BDProvincia:
    
    def __init__(self):
        #ruta de la base de datos
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        self.bbdd = sqlite3.connect(dir_path + "/Weather.db",timeout=10)
        self.bbdd.row_factory = sqlite3.Row
        self.cursor = self.bbdd.cursor()
    #formado por nombre,comunidad,codigo
    def insertDefault(self):
        self.bbdd = sqlite3.connect("Weather.db")
        self.bbdd.row_factory = sqlite3.Row
        cursor = self.bbdd.cursor()
    
        #el codigo de provincia de mdrid es 28
        self.cursor.execute("INSERT INTO Provincia VALUES ('Madrid','mad','28');")
        self.cursor.execute("INSERT INTO Provincia VALUES ('La Rioja','rio','26');")
        self.cursor.execute("INSERT INTO Provincia VALUES ('Santa Cruz de Tenerife','coo','38');")
        self.cursor.execute("INSERT INTO Provincia VALUES ('Alicante/Alacant','val','03');")
        #confirmamos
        self.bbdd.commit()
        
        
    
    def deteleContenido(self):
        self.bbdd = sqlite3.connect("Weather.db")
        self.bbdd.row_factory = sqlite3.Row
        cursor = self.bbdd.cursor()
                         
        #el codigo de provincia de mdrid es 28
        self.cursor.execute("delete from Provincia;")
        self.bbdd.commit()
        
    def selectAll(self):
                         
        #el codigo de provincia de mdrid es 28
        self.cursor.execute("select * from provincia;")
        lineas = self.cursor.fetchall()
        return lineas
    