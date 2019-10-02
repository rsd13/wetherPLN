'''
Created on Nov 17, 2018

@author: rafaelsoriadiez
'''

from src.Dataset.Fecha import Fecha
from src.Dataset.Localidad import Localidad

class Hora:

    def __init__(self):
        
        self.hora = ""
        self.fecha = ""
        self.estadoCielo = ""
        self.precipitacion = ""
        self.probPrecipitacion = ""
        self.probTormenta = ""
        self.nieve = ""
        self.probNieve = ""
        self.temperatura = ""
        self.sensTermica = ""
        self.humedadRelativa = ""
        self.direccionViento = ""
        self.velocidadViento = ""
        self.rachaMax = ""
        self.codProvincia = ""
        self.codLocalidad = ""
    
    
    #introduce esdadoCielo
    def introducirEstadoCielo(self,datos,hora):
        hora.hora = datos["periodo"]
        hora.estadoCielo = datos["descripcion"]
    
    
    def introducirPrecipitacion(self,datos,hora):
        hora.precipitacion = datos["value"]
        
    def introducirNieve(self,datos,hora):
        hora.nieve = datos["value"]
        
    def introducirTemperatura(self,datos,hora):
        hora.temperatura = datos["value"]
        
    def introducirSensTermica(self,datos,hora):
        hora.sensTermica = datos["value"]
        
        
    def introducirHumedad(self,datos,hora):
        hora.humedadRelativa = datos["value"]
        
    def introducirViento(self,datos,hora):

        hora.direccionViento = datos["direccion"][0]
        hora.velocidadViento = datos["velocidad"][0]
    
    def introducirRacha(self,datos,hora):
        hora.rachaMax = datos["value"]
        
    def introducirProbTormenta(self,datos,hora):
        hora.probTormenta = datos["value"]
        
    def introducirProbPrecipitacion(self,datos,hora):
        hora.probPrecipitacion = datos["value"]
        
    def introducirProbNieve(self,datos,hora):
        hora.probNieve = datos["value"]
        
       