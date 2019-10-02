'''
Created on Apr 19, 2019

@author: rafaelsoriadiez
'''

import pandas as pd
import numpy as np
from src.BBDD.BDHora import BDHora
from src.Datos.Hora import Hora
from src.Datos.Grado import Grado
import random
import copy

estados = {
    
    'periodo': '',
    'viento': {
        'grado':{'Calma':0,'Flojos':0,'Vientos Medios':0,'Fuertes':0,'Muy Fuertes' :0,"Huracanados":0},
        'direccion':{'N':0,'NE':0,
                     'E':0,'SE':0,
                     'S' :0,"SO":0,
                     'O' :0,"NO":0,
                    }
    },
    'rachaMax': False,
    'rachaDato': 0
            
}

estadoViento = [
    'Calma',
    'Flojos',
    'Vientos Medios',
    'Fuertes',
    'Muy Fuertes',
    'Huracanados',
]


estadoVientoDic ={
    'Calma' :0,
    'Flojos' :1,
    'Vientos Medios' :2,
    'Fuertes':3,
    'Muy Fuertes':4,
    'Huracanados':5
}

verbosDireccion = [
    "que llegan","que soplan",
    "que rolan", 
]


verbosIguales = [
    "que tienden","que predominan",
]

verbosDisminuir = [
    "que disminuye",
    "que arrecian","que cambian"
   
    
  
]

verbosAumentar = [
    "que cambian"," que aumentan",
]



adverbiosIguales = [
    "principalmente",
    
]



class Viento:
    
    def __init__(self,path,fecha):
        self.frase = ''
        self.path = path
        self.velocidad = []
        self.direccion = []
        self.racha = []
        self.horaVelocidad = []
        self.horaDireccion = []
        self.horaRacha = []
        self.estados = estados
        self.horaviento = None
        self.fecha = fecha
        self.getViento()
        
      
        
    #Metodo que consigue los datos necesario para las horas
    def getViento(self):
        
        colnames = ['provincia','fecha','frase','clase']
        total = pd.read_csv(self.path + "total.csv", names=colnames) 
        datos = pd.DataFrame(total)
        viento = datos[datos['clase']== 'viento']
        viento = datos[datos['provincia']== 'MADRID']
        
        viento = np.array(viento)
        fecha = viento[0][1]
        #fecha = "2018-11-28"
        fecha = self.fecha
        provincia = viento[0][0]
        
        try:
            bdHora = BDHora()
            viento = bdHora.getViento(provincia, fecha)
            self.velocidad = viento[0]
            self.direccion = viento[1]
            self.racha = viento[2]

        except:
            print("Error a recoger los datos de viento")
        
        
        
       
        self.splitDia()
        
        
    def splitDia(self):
        
        hora = Hora()
        self.horaVelocidad = hora
        self.horaVelocidad.splitDia(self.velocidad)
        
        
        hora = Hora()
        self.horaDireccion = hora
        self.horaDireccion.splitDia(self.direccion)
     
        hora = Hora()
        self.horaRacha = hora
        self.horaRacha.splitDia(self.racha)
        
        self.analizarViento()
        
        
    def analizarViento(self):
        
      
        madrugada = copy.deepcopy(self.estados)
        self.mirarDireccion(madrugada,self.horaDireccion.madrugada)
        self.mirarVelocidad(madrugada,self.horaVelocidad.madrugada)
        self.mirarRacha(madrugada,self.horaRacha.madrugada)
        madrugada = self.resumirPeriodo("madrugada", madrugada)
        
        mañana = copy.deepcopy(self.estados)
        self.mirarDireccion(mañana,self.horaDireccion.mañana)
        self.mirarVelocidad(mañana,self.horaVelocidad.mañana)
        self.mirarRacha(mañana,self.horaRacha.mañana)
        mañana = self.resumirPeriodo("mañana", mañana)
        
        central = copy.deepcopy(self.estados)
        self.mirarDireccion(central,self.horaDireccion.central)
        self.mirarVelocidad(central,self.horaVelocidad.central)
        self.mirarRacha(central,self.horaRacha.central)
        central = self.resumirPeriodo("horas centrales de la ", central)
        
        tarde =  copy.deepcopy(self.estados)
        self.mirarDireccion(tarde,self.horaDireccion.tarde)
        self.mirarVelocidad(tarde,self.horaVelocidad.tarde)
        self.mirarRacha(tarde,self.horaRacha.tarde)
        tarde = self.resumirPeriodo("tarde", tarde)
        
        noche =  copy.deepcopy(self.estados)
        self.mirarDireccion(noche,self.horaDireccion.noche)
        self.mirarVelocidad(noche,self.horaVelocidad.noche)
        self.mirarRacha(noche,self.horaRacha.noche)
        noche = self.resumirPeriodo("noche", noche)
        
        periodoTotal = [madrugada,mañana,central,tarde,noche]
        
        
        self.analizarPeriodos(periodoTotal)
        
       
        
        
        
        #madrugada = self.resumirPeriodo(madrugada)
    
    def analizarVientosAux(self,periodo,periodoDia,periodoTotal):
        
        self.mirarDireccion(periodo,self.horaDireccion.madrugada)
        self.mirarVelocidad(periodo,self.horaVelocidad.madrugada)
        self.mirarRacha(periodo,self.horaRacha.madrugada)
        resumen  = self.resumirPeriodo(periodoDia, periodo)
   
        periodoTotal.append(resumen)

    def mirarDireccion(self,estado,periodo):
        
        for datos in periodo:
            for k,v in datos.items():
                if v == "N":
                    estado["viento"]["direccion"]["N"] += 1
                elif v == "NE":
                    estado["viento"]["direccion"]["NE"] += 1
                elif v == "E":
                    estado["viento"]["direccion"]["E"] += 1
                elif v == "SE":
                    estado["viento"]["direccion"]["SE"] += 1
                elif v == "S":
                    estado["viento"]["direccion"]["S"] += 1
                elif v == "SO":
                    estado["viento"]["direccion"]["SO"] += 1
                elif v == "O":
                    estado["viento"]["direccion"]["O"] += 1
                elif v == "NO":
                    estado["viento"]["direccion"]["NO"] += 1
                                
    def mirarVelocidad(self,estado,periodo):
        for datos in periodo:
            for k,v in datos.items():
               
                if(int(v) <= 5):
                    estado["viento"]["grado"]["Calma"] += 1
                elif(int(v) > 5 and int(v) <= 20):
                    estado["viento"]["grado"]["Flojos"] += 1
                elif(int(v) > 20 and int(v) <= 40):
                    estado["viento"]["grado"]["Vientos Medios"] += 1
                elif(int(v) > 40 and int(v) <= 70):
                    estado["viento"]["grado"]["Fuertes"] += 1
                elif(int(v) > 70 and int(v) <= 120):
                    estado["viento"]["grado"]["Muy Fuertes"] += 1
                elif(int(v) > 120):
                   
                    estado["viento"]["grado"]["Huracanados"] += 1
     
    def mirarRacha(self,estado,periodo):
    
        for datos in periodo:
            for k,v in datos.items():
               
                if(int(v) > 70):
                 
                    estado["rachaMax"] = "Muy Fuertes"
                elif(int(v) > 120):
                    estado["rachaMax"] = "Huracanadas"
                
                if(int(v) > estado["rachaDato"] ): 
                    estado["rachaDato"] = int(v)
                             
    def resumirPeriodo(self,periodo,estados):
        resumen = {
                "periodo": periodo,
                "generalVelocidad": "",
                "generalDireccion":"",
                "generalRacha":False,
               
               
            }
        
        mayor = 0
        for k,v in estados["viento"]["grado"].items():
                if(v > mayor):
                    resumen["generalVelocidad"] = k
                   
        mayor = 0
        for k,v in estados["viento"]["direccion"].items():
                if(v > mayor):
                    resumen["generalDireccion"] = k
        
        racha = estados['rachaMax']        
        if(racha): resumen["generalRacha"] = racha 
          
        return resumen
    
    def analizarPeriodos(self,periodos):
        
        gradoViento = Grado()
        listaIgual = []
        listaDireccion = []
        
        i = 0
        igual = False
        verbo = ''
        size = len(periodos)
        while i < size:
       
            print(periodos[i])
            
            listaDireccion.append(periodos[i]["generalDireccion"])
            
            result = ''
            estado = periodos[i]["generalVelocidad"]
            
            periodoTemproral =  periodos[i]["periodo"]
           
            
            if i+1 != len(periodos):
                periodoTemproralNext =  periodos[i+1]["periodo"]
                estadoNext = periodos[i+1]["generalVelocidad"]
               
            else:
                periodoTemproralNext = periodos[i]["periodo"]
                estadoNext = periodos[i]["generalVelocidad"]
            
            #Miro si sube o baja o si es igual
            grados = self.mirarNivelGrado(estado,estadoNext)
                
            #Si es el último (noche) me da igual
            if i+1 == len(periodos):
                result = periodoTemproral + ":" + estado + ":"
            elif grados[0] > grados[1]:
                verbo = "baja"
            elif grados[0] < grados[1]:
                verbo = "sube"
                
            else:
                
                if not periodoTemproral in listaIgual:
                    listaIgual.append(periodoTemproral)
                if not periodoTemproralNext in listaIgual:
                    listaIgual.append(periodoTemproralNext)
               
                igual = True
                aux = ''
                
              
                for item in listaIgual:
                    aux += item+","
                aux = aux[: len(aux) -1]
                resultIgual = aux + ":" + estado
                i += 1
                
                #Se vuelve al principio y se salta el siguiente
                continue
            
            if igual:
                resultIgual += ":" + verbo
                igual = False 
                result = resultIgual
                listaIgual = []
            else: 
               
                result = periodoTemproral + ":" + estado + ":" + verbo
                
            gradoViento.periodoGenerar.append(result)
            i += 1
            
        gradoViento.periodoGenerar = self.juntarIugales(gradoViento.periodoGenerar)
       
        
        direccion = self.fraseDireccion(listaDireccion)
        direccion = "Vientos " + random.choice(verbosDireccion) + " del " +  direccion + " que son, "
        
        frase = self.formarFrase(gradoViento)
        self.frase = direccion + frase
        self.frase = self.frase.capitalize() + "."
       
    def fraseDireccion(self,listaDireccion):
        N = NE = E = SE = S = SO = O = NO = False
        CN= CE = CS = CO = False
       
        for v in listaDireccion:
            if v == "N": N = True
            elif v == "NE":NE = True
            elif v == "E": E = True     
            elif v == "SE": SE = True     
            elif v == "S": S =True
            elif v == "SO":SO =True  
            elif v == "O": O = True
            elif v == "NO": NO = True
            
        
        lista = []
        if N and NE and NO:
            lista.append("componente norte")
            CN = True
        elif E and SE and NE:
            lista.append("componente este")
            CE = True
        elif O and NO and SO:
            lista.append("componente oeste")
            CO = True
        elif S and SE and SO:
            lista.append("componente sur")
            CS = True
            
        if N and not CN:  lista.append("norte")
        if S and not CS:  lista.append("sur")
        if E and not CE:  lista.append("este")
        if O and not CO:  lista.append("oeste")
        if NE and not CO and not CE:  lista.append("noreste")
        if NO and not CN and not CO:  lista.append("noroeste")
        if SE and not CS and not CE:  lista.append("sureste")
        if SO and not CS and not CO:  lista.append("suroeste")
            
        i = 0
        frase = ""
        while( i < len(lista)):
            if (len(lista) > 1):
                if(i == len(lista) -1):  frase +=  " y "+ lista[i]
                else:
                    frase += lista[i]
                    if(  i != len(lista) -2 ): frase +=  ", "
                    
            else:  frase += lista[i]
            
            i +=1
        
        return frase
        
        
    def mirarNivelGrado(self,now,next):
        
        num = numNext = 0
        for k,v in estadoVientoDic.items():
                
            if(k == now): num = v
            if(k == next): numNext = v
    
        return num,numNext
    
    
    def juntarIugales(self,lista):
       
        i = 0
        aux1 = result = ''
        listaIgual= []
        newLista = []
        
        for item in lista:
            
            aux = item.split(",")
            
            #si no ha habido iguales se mira si se repite el tiempo verbal
            if len(aux) == 1:
                
                itemNow = item.split(":")
                if i+1 != len(lista):
                    itemNext = lista[i+1].split(":")
                    igual = True
                
                if igual and itemNow[2] == itemNext[2] :
                    if not itemNow[0] in listaIgual:
                        listaIgual.append(itemNow[0])
                    if not  itemNext[0] in listaIgual:
                        listaIgual.append(itemNext[0])
                else:
                    if len(listaIgual) != 0:
                        for item1 in listaIgual:
                            aux1 += item1+","
                        aux1 = aux1[: len(aux1) -1]
                       
                        result =  aux1 + ":" + itemNext[1] + ":" +  itemNext[2]
                        newLista.append(result)
                        
                    else: newLista.append(item)
                           
            else: newLista.append(item)
                
            igual = False    
            aux1 =''
            i +=1
        
        return newLista
    

    
    def formarFrase(self,gradoNubes):
        
        i = 0
        fenomeno = frase = prep = tiempo = ''
        lista = gradoNubes.periodoGenerar
        size = len(lista)
        print(lista)
        while i < size:
           
            item = lista[i].split(":")
            periodos =  item[0].split(",")
            periodos = gradoNubes.mirarPeriodo(periodos)
            
            
            if item[1] == "Calma":
                fenomeno= item[1] = "Vientos con calma"
            else:
                fenomeno = item[1] = "Vientos " + item[1]
            fenomeno = item[1]
        
            
            if item[2] == "sube":
                tiempo = random.choice(verbosAumentar)
            else:
                tiempo =  random.choice(verbosDisminuir)
            
            
            if size == 1:
                frase += fenomeno + " durante todo el día"
                
            elif size == 2:
                if i == 0:
                    prep = " a "
                    frase += fenomeno + " " + periodos + " " + tiempo + prep
                else:
                    frase += fenomeno + " " + periodos 
                
            else:
                if i +2  == size:
                   
                    prep = " y "
                    frase += fenomeno + " " + periodos + " " + prep +  tiempo + " a "
                elif i + 1 == size:
                    
                    frase += fenomeno + " " + periodos 
                else:
                    prep = " a "
                    frase += fenomeno + " " + periodos + " " + tiempo + prep
            
            i +=1
            prep = ""
        
       
        return frase
        
                    
        
        
        