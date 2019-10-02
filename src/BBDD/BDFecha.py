'''
Created on Nov 17, 2018

@author: rafaelsoriadiez
'''

import sqlite3
import os
from src.Dataset.Fecha import Fecha

#DIA MES AÑO
class BDFecha:
    
    def __init__(self):
        #ruta de la base de datos
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        self.bbdd = sqlite3.connect(dir_path + "/Weather.db",timeout=10)
        self.bbdd.row_factory = sqlite3.Row
        self.cursor = self.bbdd.cursor()
        
    
    
    def insertFecha(self,fecha):
        self.cursor.execute("select * " + 
                            "from fecha " +
                            "where dia= " + fecha.dia + " and mes=" + fecha.mes + 
                            " and año=" + fecha.año + ";")
        
        lineas = self.cursor.fetchall()
        
        #si no existe esa fecha se inserta
        if len(lineas) == 0:
            self.cursor.execute("INSERT INTO fecha VALUES ("+  fecha.dia + "," + fecha.mes +
                                "," + fecha.año + ");")
            self.bbdd.commit()
            
            
    
            
            