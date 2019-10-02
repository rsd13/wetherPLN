'''
Created on Nov 19, 2018

@author: rafaelsoriadiez
'''

import sqlite3
import os
from src.Dataset.Fecha import Fecha


class BDTextoProvincia:
    #formado por nombre,codProvincia,codigo
    
    def __init__(self):
        #ruta de la base de datos
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        self.bbdd = sqlite3.connect(dir_path + "/Weather.db",timeout=10)
        self.bbdd.row_factory = sqlite3.Row
        self.cursor = self.bbdd.cursor()
        
        
    def insertTexto(self,fecha,codigoProvincia,codigoComunidad,texto):
        #comprobamos si existe
        self.cursor.execute("select * " + 
                            "from textoprovincia " +
                            "where dia=? and mes=? and año=? and codigoProvincia=?" +
                            " and codigoComunidad=?",(
                            fecha.dia,
                            fecha.mes,
                            fecha.año,
                            codigoProvincia,
                            codigoComunidad))
         
        lineas = self.cursor.fetchall()
        
        #si no existe se inserta
        if len(lineas) == 0:
            self.cursor.execute("INSERT INTO textoprovincia VALUES (?,?,?,?,?,?)",(
                fecha.dia,
                fecha.mes,
                fecha.año,
                codigoProvincia,
                codigoComunidad,
                texto))
                
               
             
            self.bbdd.commit()