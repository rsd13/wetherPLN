'''
Created on Nov 18, 2018

@author: rafaelsoriadiez
'''
import sqlite3
import os



class BDLocalidad:
    #formado por nombre,codProvincia,codigo
    
    def __init__(self):
        #ruta de la base de datos
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        self.bbdd = sqlite3.connect(dir_path + "/Weather.db",timeout=10)
        self.bbdd.row_factory = sqlite3.Row
        self.cursor = self.bbdd.cursor()
        
    def insertDefaultMadrid(self):
        
        #el codigo de provincia de mdrid es 28
        self.cursor.execute("INSERT INTO Localidad VALUES ('Madrid','28','079');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Alcalá de Henares','28','005');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Getafe','28','065');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Collado Villalba','28','047');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Navalcarnero','28','096');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Aranjuez','28','013');")
        
        #confirmamos
        self.bbdd.commit()
        
        
    def insertDefaultRioja(self):
        self.cursor.execute("INSERT INTO Localidad VALUES ('Haro','26','071');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Calahorra','26','036');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Logroño','26','089');")
        
        #confirmamos
        self.bbdd.commit()
        
        
    def insertDefaultCanaria(self):

        self.cursor.execute("INSERT INTO Localidad VALUES ('Santa Cruz de Tenerife','38','038');")    
        #confirmamos
        self.bbdd.commit()
        
        
    def insertDefaultAlicante(self):
                                 
        #el codigo de provincia de mdrid es 28
        self.cursor.execute("INSERT INTO Localidad VALUES ('Alicante/Alacant','03','014');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Orihuela','03','099');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Dénia','03','063');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Elche/Elx','03','065');")
        self.cursor.execute("INSERT INTO Localidad VALUES ('Alcoy/Alcoi ','03','009');")      
        #confirmamos
        self.bbdd.commit()
        
        
    def deteleContenido(self):
                                 
        #el codigo de provincia de mdrid es 28
        self.cursor.execute("delete from Localidad;")
        self.bbdd.commit()
        
    def selectAll(self):
                         
        #el codigo de provincia de mdrid es 28
        self.cursor.execute("select * from localidad;")
        lineas = self.cursor.fetchall()
        return lineas
        
    def insertDefault(self):    
        self.insertDefaultMadrid()
        self.insertDefaultRioja()
        self.insertDefaultCanaria()
        self.insertDefaultAlicante()