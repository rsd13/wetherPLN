'''
Created on Nov 17, 2018

@author: rafaelsoriadiez
'''

from src.Dataset.Provincia import Provincia

class Localidad:

    def __init__(self, codigo,nombre,comunidad):
        self.codigo = codigo
        self.nombre = nombre
        self.comunidad = comunidad