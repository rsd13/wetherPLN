'''
Created on May 3, 2019

@author: rafaelsoriadiez
'''


import pandas as pd
import numpy as np
from src.BBDD.BDHora import BDHora
from src.Datos.Hora import Hora
from src.Datos.Grado import Grado
import random
import copy
from bokeh.util.session_id import random


estados = {
    'periodo': '',
    'heladas':False
}






class Temperatura:
    def __init__(self,path,fecha):
        self.frase = ""
        self.fraseHelada = ""
        self.path = path
        self.estados = estados
        self.horaTemperatura = None
        self.fraseTablaTemperatura = ''
        self.fecha = fecha
        self.getTemperatura()
        
        
        
    def getTemperatura(self):
        colnames = ['provincia','fecha','frase','clase']
        total = pd.read_csv(self.path + "total.csv", names=colnames) 
        datos = pd.DataFrame(total)
        viento = datos[datos['clase']== 'viento']
        viento = datos[datos['provincia']== 'MADRID']
        
        viento = np.array(viento)
        fecha = viento[0][1]
        '''
        fechaNow = "2018-12-28"
        fechaOld = "2018-12-27"
        '''
        fechaNow = self.fecha
        fechaOld = "2018-12-16"
        #fecha = "2018-11-22"
        provincia = viento[0][0]
        temperaturaNow = []
        
        try:
            bdHora = BDHora()
            temperaturaNow = bdHora.getTemperatura(provincia, fechaNow,True)
            temperaturaOld = bdHora.getTemperatura(provincia, fechaOld,True)
            temperatura =  bdHora.getTemperatura(provincia, fechaNow,False)
            print("-----")
           
        except:
            print("Error a recoger los datos de temperatura")
            
        
        self.definirHeladas(temperatura)
        self.tablaTemperatura(temperaturaNow)
       
        self.diferenciaTemperatura(temperaturaNow, temperaturaOld)
       
        
        #self.analizarMaximosMinimos(temperatura)
            
  
    def tablaTemperatura(self,temperatura):
        pass
        
        frase = "TEMPERATURAS MÍNIMAS Y MÁXIMAS PREVISTAS (C):\n"
       
        for item in temperatura:
            item = item.split(":")
            ciudad = item[0]
            mayor = item[1]
            menor = item[2]
            
            frase += ciudad 
            
            espacios = ""
            
            i = len(ciudad)
            while i < 35:
                espacios +=  " "
                i += 1
               
            if int(menor) < 0 or int(mayor) < 0:
                size = len(espacios)
                espacios = espacios[:size - 1]
                
            frase += espacios + menor + "     " + mayor +"\n"
                

        self.fraseTablaTemperatura = frase
        
        
    def analizarTemperatura(self,temperatura):
        
        
        for dic1 in temperatura:
            for k1,v1 in dic1.items():
                for dic2 in v1:
                   for k1,v2 in dic2.items():
                       if v2 < "0":
                           pass
                          
        return False
        
            
            
    def splitDia(self,temperatura):
        
        for dic1 in temperatura:
            for k1,v1 in dic1.items():
                for dic2 in v1:
                   for k1,v2 in dic2.items():
                       if v2 < "0":
                           pass
                           
    
    def analizarMaximosMinimos(self,temperatura):
        pass
        
    def diferenciaTemperatura(self,listNow,listOld):
        fraseMayor = fraseMenor = frase = ""
        #Busco la mayor de todas y la menor de todas
        now = (0,0)
        old = (0,0)
        frase = "Temperaturas con "
        now = self.mayorMenor(listNow)
        old = self.mayorMenor(listOld)
        listaPocos = ["pocos cambios", "cambios ligeros", "débiles cambios"]
                
       
        #Resto los mayores y los menores
        
        if now[0] > old[0]:
            restaMayor = now[0] - old[0]
            
            fraseMayor = self.verDiferencia(restaMayor, "sube",True)
        else: 
            restaMayor = old[0] - now[0]
            fraseMayor = self.verDiferencia(restaMayor, "baja",True)
            
        restaMenor = 0
        
        if now[1] < old[1]:
            restaMenor =abs(now[1]) - abs(old[1])
            fraseMenor = self.verDiferencia(restaMenor, "baja",False)
        else: 
            restaMenor = abs(old[1]) - abs(now[1])
            fraseMenor = self.verDiferencia(restaMenor, "sube",False)
        
        
        
        if fraseMayor == "" and fraseMenor == "":
            frase += random.choice(listaPocos)
        elif fraseMayor== "" and fraseMenor != "":
            frase += fraseMenor
        elif fraseMayor!= "" and fraseMenor == "":
            frase +=  fraseMayor
        else:
            frase += fraseMayor + " y "  + fraseMenor
        
        
        self.frase =  frase + self.fraseHelada + "."
       
        
    def mayorMenor(self,lista):
        result = ()
        mayorNow = -999
        menorNow = 999
        for item in lista:
            item = item.split(":")
            mayor = int(item[1])
            menor = int(item[2])
            if mayor > mayorNow:
                mayorNow = mayor
            if menor < menorNow:
                menorNow = menor
      
        
        result=( mayorNow,menorNow)
        
        return result
    
    def verDiferencia(self,dato,verbo,esMaxima):
        
        frase = ""
        
        fraseMaxima = "máximas"
        
        if not esMaxima:
            fraseMaxima = "mínimas"
            
            
        if verbo == "sube":
            verbos = ["aumento", "incremento"]
            verbo = random.choice(verbos)
        else:
            verbos = ["descenso", "bajadas"]
            verbo = random.choice(verbos)
        
        if dato <= 2:
            return ""
        elif dato >= 3 and dato <=5:
        
            frase =  verbo + " de " + fraseMaxima
        elif dato >= 6 and dato <=10:
            adjetivos = ["notable", "alto","significativo"]
            frase = verbo + " "  + random.choice(adjetivos) + " de " + fraseMaxima
        elif dato > 10:
            frase = verbo + " extraordinario de  " + fraseMaxima
        

        return frase
    
    
    def definirHeladas(self,dic):
        heladas = ['','','']
       
        for v in dic:
            temp = int(v)
            
            if temp < 0 and temp >= -4:
                
                heladas[0] = "débiles"
            elif temp <-4 and temp >= -8:
                heladas[1] = "normal"
            elif temp < -8:
                heladas[2] = "fuertes"
                
        frase = adjetivo = ""
        
        
        for helada in heladas:
            if helada != "":
                adjetivo = helada
                
        
        if adjetivo =="normal":
            frase = "heladas"
            
        elif adjetivo =="fuertes":
            listaAdjetivos = ["fuertes","intensas","grandes","significativas"]
            adjetivo = random.choice(listaAdjetivos)
            frase = "heladas " + adjetivo
        elif adjetivo =="débiles":
            frase = "heladas débiles"
            
        if frase != "":

            self.fraseHelada = " con " + frase
        