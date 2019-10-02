'''
Created on Mar 29, 2019

@author: rafaelsoriadiez
'''



import pandas as pd
import numpy as np
from src.BBDD.BDHora import BDHora
from src.Datos.Hora import Hora
from src.Datos.Grado import Grado, verbosDisminuir
import random
import copy
from _ast import Num

#http://www.aemet.es/es/eltiempo/prediccion/espana/ayuda
estadoCielo = [
    'Despejado',
    'Poco nuboso',
    'Intervalos nuboso',
    'Nuboso',
    'Muy nuboso',
    'Cubierto',
]


estadoCieloDic = {
    'Despejado:':0,
    'Poco nuboso':1,
    'Intervalos nuboso':2,
    'Nuboso':3,
    'Muy nuboso':4,
    'Cubierto':5,
}





estados = {
    'periodo': '',
    'despejado': 0,
    'nubes': {
        'nubes': 0,
        'estado':{'Poco nuboso':0,'Intervalos nuboso':0,'Nuboso':0,'Muy nuboso':0,'Cubierto' :0 },
        'lluvia':False,
        'nieve':False,
    },
    'nubesAltas': False
}


verbosIguales = [
    "que tienen","que predominan",
    "que esperan", 
]

verbosDisminuir = [
    "que se despejan",
    "que disminuyen","que cambian",
    "que alternan"
    
]

verbosAumentar = [
    "que crece","que aumenta",
    "que incrementa","que alternan",
    "que cambian"
]

class Nubes:
    
    def __init__(self,path,fecha):
        self.frase = ''
        self.path = path
        self.nubes = []
        self.estados = estados
        self.horaNubes = None
        self.fecha = fecha
        self.getNubes()
        
        
    #Metodo que consigue los datos necesario para las horas
    def getNubes(self):
        
        colnames = ['provincia','fecha','frase','clase']
        total = pd.read_csv(self.path + "total.csv", names=colnames) 
        datos = pd.DataFrame(total)
        nubes = datos[datos['clase']== 'nubes']
        nubes = datos[datos['provincia']== 'ALACANT/ALICANTE']
        #2018-12-17" despejado todo
        nubes = np.array(nubes)
        fecha = nubes[0][1]
        fecha = self.fecha
        #fecha = "2018-11-25"
        
        provincia = nubes[0][0]
        
        try:
            bdHora = BDHora()
            nubes = bdHora.getNube(provincia, fecha)
            self.nubes = nubes      
        except:
            print("Error a recoger los datos de precipitación")
            
        
            
        self.splitDia()
        
        
       
            
            
    def splitDia(self):  
        
       
        hora = Hora()
        self.horaNubes = hora
        self.horaNubes.splitDia(self.nubes)
        self.analizarNubes()
        
        
    
    def analizarNubes(self):
        
        madrugada = copy.deepcopy(self.estados)
       
        self.mirarNubes(madrugada,self.horaNubes.madrugada)
        madrugada["periodo"] = "madrugada"       
        madrugada = self.resumirPeriodo(madrugada)
        
       
        
        mañana = copy.deepcopy(self.estados)
        self.mirarNubes(mañana,self.horaNubes.mañana)
        mañana["periodo"] = "mañana"
        mañana = self.resumirPeriodo(mañana)
        
        central = copy.deepcopy(self.estados)
        self.mirarNubes(central,self.horaNubes.central)
        central["periodo"] = "horas centrales de la "
        central = self.resumirPeriodo(central)
        
        tarde = copy.deepcopy(self.estados)
        self.mirarNubes(tarde,self.horaNubes.tarde)
        tarde["periodo"] = "tarde"
        tarde = self.resumirPeriodo(tarde)
        
        noche = copy.deepcopy(self.estados)
        self.mirarNubes(noche,self.horaNubes.noche)
        noche["periodo"] = "noche"
        noche = self.resumirPeriodo(noche)
        
        #Creo una lista con todo el dia y lo analizo, sabiendo que la posicion es:
        #madrugada, mañana, central, tarde y noche (orden del dia
        lista = [madrugada,mañana,central,tarde,noche]
        
        self.analizarPeriodos(lista)
        
    
    
    def resumirPeriodo(self,periodo):
        resumen = {
                "periodo": periodo["periodo"],
                "mayor": "",
                "menor":"",
                "general":"",
                "lluvia":False,
                "nieve":False,
                "altas":False
        }
        
        despejado = periodo["despejado"]
        nubes = periodo["nubes"]["nubes"]
        
        primero = True
       
        if despejado < nubes:
            
            if  periodo["nubes"]["lluvia"]: resumen["lluvia"] = True
            elif periodo["nubes"]["nieve"]: resumen["nieve"] = True
            
            #miro el mayor de nubes
            old = 0
            for dato,veces in periodo["nubes"]["estado"].items():
                #Me quedo con la que mas veces tiene
                
                if (veces > old):
                    resumen["general"] = dato
                #Me quedo con la mayor, puesto que esta en orden 
                if (veces > 0):
                    resumen["mayor"] = dato
                    
                    
                if veces > 0 and primero:
                    resumen["menor"] = dato
                    primero = False
                
                old = veces
                
        else: resumen["general"] = "Despejado"
        if periodo["nubesAltas"]: resumen["altas"]: True

        return resumen
                    
    def mirarNubes(self,estado,periodo):
        
        for item  in periodo:
            for hora, dato in item.items():
               
                #Miro si hay nubes
                if(dato.find("nuboso") != -1 or (dato.find("cubierto") != -1 or
                   dato.find("Nuboso") != -1 )):
                    estado["nubes"]["nubes"] +=1 
                    fraseLLuvia = fraseNieve = ""
                    
                    #Miramos si hay lluvia o no
                    if(dato.find("lluvia") != -1): 
                        estado["nubes"]["lluvia"] = True
                        fraseLLuvia = " con lluvia"
                        
                    elif(dato.find("nieve") != -1 ): 
                        estado["nubes"]["nieve"] = True
                        fraseNieve = " con nieve"
                  
                    if(dato.find("Poco nuboso") != -1):
                        estado["nubes"]["estado"]["Poco nuboso"] += 1
                
                    elif(dato.find("Intervalos nuboso") != -1):
                        estado["nubes"]["estado"]["Intervalos nuboso"] += 1
                    elif(dato.find("Nuboso") != -1):
                        estado["nubes"]["estado"]["Nuboso"] += 1
                        
                    elif(dato.find("Muy nuboso") != -1):
                        estado["nubes"]["estado"]["Muy nuboso"] += 1
                    
                    elif(dato.find("Cubierto") != -1):
                        estado["nubes"]["estado"]["Cubierto"] += 1
                
                elif(dato.find("Despejado")  != -1):
                    estado["despejado"] +=1
                
                elif(dato.find("Nubes altas")  != -1):
                    estado["NubesAltas"] = True
                    
    def analizarPeriodos(self,periodos):
        
        
        gradoNubes = Grado()
        i = 0
        igual = False
        listaIgual = []
        verbo = resultIgual = ''
      
        while i < len(periodos):
            
            result = ''
            estado = periodos[i]["general"]
            periodoTemproral =  periodos[i]["periodo"]
            
            if i+1 != len(periodos):
                periodoTemproralNext =  periodos[i+1]["periodo"]
                estadoNext = periodos[i+1]["general"]
            else:
                periodoTemproralNext = periodos[i]["periodo"]
                estadoNext = periodos[i]["general"]
            
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
            else: result = periodoTemproral + ":" + estado + ":" + verbo
            gradoNubes.periodoGenerar.append(result)
            
            i += 1
           
            
       
        
        size = len(gradoNubes.periodoGenerar )
        
        if size <=3:
            #Juntamos los tiempos verbales iguales 
            gradoNubes.periodoGenerar  = self.juntarIugales(gradoNubes.periodoGenerar)
            
        self.formarFrase(gradoNubes)
        
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

    def mirarNivelGrado(self,now,next):
        
        num = numNext = 0
        for k,v in estadoCieloDic.items():
                
            if(k == now): num = v
            if(k == next): numNext = v
    
        return num,numNext
        
    
      
            
    def formarFrase(self,gradoNubes):
        
        i = 0
        fenomeno = frase = prep = tiempo = ''
        lista = gradoNubes.periodoGenerar
        size = len(lista)
        while i < size:
            item = lista[i].split(":")
            periodos =  item[0].split(",")
            periodos = gradoNubes.mirarPeriodo(periodos)
            
            if item[1] == "Intervalos nuboso":
                fenomeno= item[1] = "Intervalos nubosos"
            else:
                fenomeno = item[1] = "cielos " + item[1] + "s"
            
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
                   
                    prep = ",y "
                    frase += fenomeno + " " + periodos + " " + prep +  tiempo + " a "
                elif i + 1 == size:
                    
                    frase += fenomeno + " " + periodos 
                else:
                    prep = " a "
                    frase += fenomeno + " " + periodos + " " + tiempo + prep
            
            i +=1
            prep = ""
        
        self.frase = frase.capitalize() +"."
        print(self.frase)
    
                    
                    

        