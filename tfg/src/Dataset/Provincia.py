'''
Created on Nov 17, 2018

@author: rafaelsoriadiez
'''
from .Comunidad import Comunidad

class Provincia:

    def __init__(self, codigo,nombre,comunidad):
        self.codigo = codigo
        self.nombre = nombre
        self.comunidad = comunidad