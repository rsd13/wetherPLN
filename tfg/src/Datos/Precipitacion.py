'''
Created on Apr 3, 2019

@author: rafaelsoriadiez
'''

import pandas as pd
import numpy as np
from src.BBDD.BDHora import BDHora
from src.Datos.Hora import Hora
from src.Datos.Grado import Grado
import random
import copy
from src.Datos.Nubes import verbosAumentar


verbosDisminuir = [
    "que disminuyen","que disipan",
    "que remiten","que bajan",
    
]

verbosDesaparecer = [
    "que desaparecen","que se descartan"
]

verbosLLovizna = [
    "se esperan","que afectan",
]

estadosProbabilidad = {
    'probabilidadTemporal': ['','',''],
    'probabilidadEspacial': ['',''],
    'probabilidad': ['','',''],

    
}

estados = {
    
    'periodo':'',
    'lloviznas':False,
    #Si esta en False no hay precipitaciones ese dia.
    'lluvias': {'existe':False,'Débiles':0,'Lluvias':0,'Fuertes':0,'Muy Fuertes' :0,"Torrenciales":0},
    'chubascos': {'existe':0,'Chubascos':0,'Fuertes':0,'Muy Fuertes' :0,"Torrenciales":0},
    
}

estadoPrecipitacion = [
    'Débiles',
    'Fuertes',
    'Lluvias',
    'Chubascos',
    'Muy Fuertes',
    'Nuboso',
    'Torrenciales',
]


grados = {
    
    'Débiles': 1,
    'Lluvias Medias': 2,
    'Fuertes':3,
    'Muy Fuertes':4,
    'Torrenciales':5
}


probTormenta = ['','','']


class Precipitacion:
    
    def __init__(self,path,fecha):
        self.frase = ''
        self.path = path
        self.precipitacion = []
        self.probPrecipitacion = []
        self.probTormenta = []
        self.nieve = []
        self.probNieve = []
        self.horaPrecipitacion = None
        self.horaProbPrecipitacion = None
        self.horaProbTormenta = None
        self.estados = estados
        self.fecha = fecha
        self.getPrecipitacion()
        
        
        
        
        
    #Metodo que consigue los datos necesario para las horas
    def getPrecipitacion(self):


        
        colnames = ['provincia','fecha','frase','clase']
        total = pd.read_csv(self.path + "total.csv", names=colnames) 
        datos = pd.DataFrame(total)
        precipitacion = datos[datos['clase']== 'precipitacion']
        precipitacion = datos[datos['provincia']== 'MADRID']
        
        precipitacion = np.array(precipitacion)
        fecha = precipitacion[0][1]
        fecha = self.fecha
        #fecha = "2018-11-25"
        provincia = precipitacion[0][0]
        
        try:
            bdHora = BDHora()
            precipitacion = bdHora.getPrecipitacion(provincia, fecha)
            self.precipitacion = precipitacion[0]
            self.probPrecipitacion = precipitacion[1]
            self.probTormenta = precipitacion[2]
            self.nieve = precipitacion[3]
            self.probNieve = precipitacion[4]
            
        except:
            print("Error a recoger los datos de precipitación")
            
            
       

        self.splitDia()
        
         
    #Metodo que divide las horas por los periodos establecidos
    def splitDia(self):  
        
       
        hora = Hora()
        self.horaPrecipitacion = hora
        self.horaPrecipitacion.splitDia(self.precipitacion)
        
        hora = Hora()
        self.horaProbPrecipitacion = hora
        self.horaProbPrecipitacion.splitDia(self.probPrecipitacion)
        
        self.analizarPrecipitacion()
          
    def analizarPrecipitacion(self):
        frase = ''
        temporal = 0
        
        madrugada = copy.deepcopy(self.estados)
        temporal += self.mirarPrecipitacion(self.horaPrecipitacion.madrugada, madrugada)
        madrugada = self.hacerResumen("madrugada",madrugada)
        
        mañana = copy.deepcopy(self.estados)
        temporal +=self.mirarPrecipitacion(self.horaPrecipitacion.mañana, mañana)
        mañana = self.hacerResumen("mañana",mañana)
        
        central = copy.deepcopy(self.estados)
        temporal +=self.mirarPrecipitacion(self.horaPrecipitacion.central, central)
        central = self.hacerResumen("horas centrales de la ",central)
        
        tarde = copy.deepcopy(self.estados)
        temporal +=self.mirarPrecipitacion(self.horaPrecipitacion.central, tarde)
        tarde = self.hacerResumen("tarde",tarde)
        
        noche = copy.deepcopy(self.estados)
        temporal +=self.mirarPrecipitacion(self.horaPrecipitacion.central, noche)
        noche = self.hacerResumen("noche",noche)
        
        self.probabilidadTemporal(5, temporal)
        self.mirarProbabilidad()
       
       
        periodoTotal = [madrugada,mañana,central,tarde,noche]
        
        
        self.analizarPeriodos(periodoTotal)
        #self.analizarResumen(periodoTotal)
         
    def hacerResumen(self,periodo,estado):
        resumen = {
                "periodo": periodo,
                "llovizna":False,
                "generalLluvia":False,
                "generalChubascos":False,
                "formenta":False
                
        }
        
        if(estado["lloviznas"]): resumen["llovizna"] = "lloviznas"
        
       #Miro los chubascos
       
        if estado["chubascos"]["existe"] > 0:
           
            old = -1
            for k,v in estado["chubascos"].items():
                if k != "existe":
                  
                    if v > old:
                        resumen["generalChubascos"] = k
                    
                    #Me quedo con el mayor, es decir, el último
                  
                    old = v
                
        
        #Miro las lluvias si hay
        if estado["lluvias"]["existe"]:
          
            old = -1
            for k,v in estado["lluvias"].items():
                if k != "existe":
              
                    if v > old:
                        resumen["generalLluvia"] = k
                    
                    #Me quedo con el mayor, es decir, el último
                  
                    old = v
        
       
        return resumen
    
    def mirarProbabilidad(self):
        
        for periodo in self.horaProbPrecipitacion.total:
            for k,v in periodo.items():
               self.mirarProbabilidadPrec(v)
          
    def mirarPrecipitacion(self,periodo,estados):
        probabilidadEspacial = 0
        sumProbabilidadEspacial = 0
        totalEspacial = len(periodo)
        probabilidadTemporal = 0
        
        old = "0"
        for dic in periodo:
            
            for k,v in dic.items():
               

                if v == "Ip":
                    estados["lloviznas"]= True
                    probabilidadEspacial = 1
                    probabilidadTemporal = 1
                #Si los dos tienen valor es lluvia, sino, es chubascos
                elif v != "0" and old != "0":
                    #Primero se resta el anterior de chubascos
                  
                    self.rangoChubascos(old,estados,"restar")
                    self.rangoLLuvia(v,estados)
                    probabilidadEspacial = 1
                    probabilidadTemporal = 1
                    
                #Se pone de momento en chubascos
                elif v != "0":
                    self.rangoChubascos(v,estados,"sumar")
                    probabilidadEspacial = 1
                    probabilidadTemporal = 1
                
                if v == "Ip": old = "0"
                else: old = v
            
            sumProbabilidadEspacial += 1
            
        self.probabilidadEspacial(len(periodo), sumProbabilidadEspacial)
        return probabilidadTemporal
                     
    def verPeriodos(self,periodo,estado,grado):
        periodoTemproral =  periodo["periodo"]
        if estado in grado.periodoLluvias:
            if not periodoTemproral in  grado.periodoLluvias[estado]:
                grado.periodoLluvias[estado].append(periodoTemproral)
        else:
            grado.periodoLluvias[estado] = []
            if(periodoTemproral != ''): grado.periodoLluvias[estado].append(periodoTemproral)
          
    def rangoChubascos(self,dato,estados,operacion):
        if(operacion == "sumar"): estados["chubascos"]["existe"] += 1
        if(operacion == "restar"): estados["chubascos"]["existe"] -= 1
        
        if dato <= "1.5":
            if(operacion == "sumar"): estados["chubascos"]["Chubascos"] +=1 
            if(operacion == "restar"):  estados["chubascos"]["Chubascos"] -=1 
            
        elif dato > "1.5" and dato < "3":
            if(operacion == "sumar"): estados["chubascos"]["Fuertes"] +=1 
            if(operacion == "restar"):  estados["chubascos"]["Fuertes"] -=1 
           
        elif dato > "3" and dato < "6":
            if(operacion == "sumar"): estados["chubascos"]["Muy Fuertes"] +=1 
            if(operacion == "restar"):  estados["chubascos"]["Muy Fuertes"] -=1 
        elif dato > "6":
            if(operacion == "sumar"): estados["chubascos"]["Torrenciales"] +=1 
            if(operacion == "restar"):  estados["chubascos"]["Torrenciales"] -=1 
                                 
    def rangoLLuvia(self,dato,estados):
        estados["lluvias"]["existe"] = True
        
        if dato >= "0" and dato <= "0.2":
            estados["lluvias"]["Débiles"] +=1 
          
        
        elif dato > "0.2" and dato < "1.5":
             estados["lluvias"]["Lluvias"] +=1 
            
            
        elif dato >= "1.5" and dato < "3":
            estados["lluvias"]["Fuertes"] +=1 
           
        elif dato >= "3" and dato < "6":
            estados["lluvias"]["Muy Fuertes"] +=1 
           

        elif dato >= "6":
            estados["lluvias"]["Torrenciales"] +=1 
                
    def probabilidadEspacial(self,total,dato):        
        listaBaja = ["aisladas","dispersas"]
        
        if(dato < total*0.3):          
            estadosProbabilidad["probabilidadEspacial"][0] = random.choice(listaBaja)
        elif(dato >= total*0.3 and dato < total*0.6):          
            pass
        elif (dato >=  total*0.6):
            estadosProbabilidad["probabilidadEspacial"][1] = "generalizadas"
               
    def probabilidadTemporal(self,total,dato):
        listaMedia = ["persistentes","continuas"]
        
       
        if(dato < total*0.3):
            estadosProbabilidad["probabilidadTemporal"][0] = "ocasionales" 
        elif(dato >= total*0.5 and dato <= total*0.59):
            estadosProbabilidad["probabilidadTemporal"][1] = "intermitentes"
        elif (dato >  total*0.6):
             estadosProbabilidad["probabilidadTemporal"][2] = random.choice(listaMedia)
        return ""
   
    def mirarProbabilidadPrec(self,dato):
        listaBaja = ["baja probabilidad",
                     "poca probabilidad",
                     "pequeña probabilidad",
                     "escasa probabilidad"]
        
        if dato >= "10" and  dato <= "40":
            estadosProbabilidad["probabilidad"][0] = "con " + random.choice(listaBaja)
        elif dato > "40" and  dato <= "70":
            estadosProbabilidad["probabilidad"][1] = "probables"
        elif dato > "70" :
            pass
            
    #Función que efectua agrupo los grados por periiodos
    def analizarPeriodos(self,periodoTotal):
        frase = ""
        probabilidad = ''
        gradoLluvia = Grado()
        gradoChubasco = Grado()
        gradoLlovizna = Grado()
        listasFrase = []
        
        for periodo in periodoTotal:
            estado = periodo["generalLluvia"]
            if(estado != False):
                self.verPeriodos(periodo, estado, gradoLluvia)
            estado = periodo["generalChubascos"]
            if(estado != False):
                self.verPeriodos(periodo, estado, gradoChubasco)
            estado = periodo["llovizna"]
            if(estado != False):
                self.verPeriodos(periodo, estado, gradoLlovizna)
                
       
        
        fraseLlovizna = self.estructurarFrase(gradoLlovizna,"lloviznas")
        if fraseLlovizna != '': listasFrase.append(fraseLlovizna)
        
        fraseLluvia = self.estructurarFrase(gradoLluvia,"lluvias")
        if fraseLluvia != '': listasFrase.append(fraseLluvia)
        
        fraseChubascos = self.estructurarFrase(gradoChubasco,"chubascos")
        if fraseChubascos != '': listasFrase.append(fraseChubascos)
    
        if len(listasFrase ) > 0:
            probabilidad = self.hacerFraseProbabilidad()
         
            frase = self.juntarFrase(listasFrase)
        else:
            self.frase = ""
        
        if frase != "" or probabilidad != "":
            self.frase = probabilidad.capitalize() + " " + frase.capitalize()
        else: self.frase = ""
       
    
    def hacerFraseProbabilidad(self):
        frase = "Precipitaciones"
        aux = ""
        i = 0
        
        #Miro si probabilidad esta vacia
        
        veces = 0
        for item in estadosProbabilidad["probabilidad"]:
            if(item == ""): vece = 1
            
        if(veces == 0): estadosProbabilidad.pop('probabilidad', None)

            
       
        for k,v in estadosProbabilidad.items():
            aux = ""
            for item in v:
                
                if item != "" : aux = item
            
            
            if( i + 1 == len( estadosProbabilidad )): 
                size = len(frase)
                frase = frase[:size - 1]
                frase += " y " + aux
            else: frase += " " + aux + ","
            
           
            i= i+1
        
       
        return  frase + "."
         
    
    def estructurarFrase(self,grado,fenomeno):
       
       
        frase = ""
        lista = grado.periodoLluvias
        if fenomeno == "lluvias" or fenomeno == 'chubascos':
            
            lista = grado.ordenarReversedGrado(lista,estadoPrecipitacion)
         
       
       
        i = 0
        
       
        #lista = {'Fuertes': ['noche'],  'Lluvias': ['mañana', 'horas centrales de la ', 'tarde', 'noche'], 'Débiles': ['madrugada']}
       
        gradoFenomeno = ""
        for k,v in lista.items():
            
            if fenomeno == "lloviznas":
               
                frase = "se esperan lloviznas"
                periodo = grado.mirarPeriodo(v)
                frase = frase + " " + periodo
                
                return frase
            
            elif (k == 'Lluvias' or k == 'Chubascos') and i==0 :
               
                frase = fenomeno 
            elif i ==0:
                frase = fenomeno + " " +  k
            
            
            periodo = grado.mirarPeriodo(v)
            
            verbo = random.choice(verbosDisminuir)
            
            if i > 0:
                conj = "a "
                
                if k == 'Lluvias' or k == 'Chubascos':
                    gradoFenomeno == ""
                else: gradoFenomeno = conj +  fenomeno  + " " + k
            
          
            if len(lista) >= 3 and i+2 == len(lista):
                frase += gradoFenomeno +  " " + periodo + " ;y "+ verbo + " "
            
            elif i+1 == len(lista):
                frase += gradoFenomeno +  " " + periodo
            else:
               frase += gradoFenomeno +  " " + periodo + " "+ verbo + " "
            
            
            
           
            
            
            i = i + 1
            
       
        return frase
            
            
            
            
    
    def estructurarFrase1(self,grado,fenomeno):
        frase = periodo = ""
        verbos = None
       
        #Si solo tiene una longitud no se mira los periodos o menor y mayor.
        
        if len( grado.periodoGenerar) == 0  :
            return ""
        elif len( grado.periodoGenerar) == 1  :
            for k,v in grado.periodoGenerar.items():
                periodo = grado.mirarPeriodo(v)
                if(k == "lloviznas" or k == "Chubascos" or k == "Lluvias"): fenomeno = ""
                frase = fenomeno + " " +  k + " "  +  random.choice(grado.adverbiosGeneral) + " "  + periodo 
        
        else:
            if(self.forma == 0): 
                verbos = grado.verbosAumentar
                dic = grado.ordenarGrado(grado.periodoGenerar,estadoPrecipitacion)
                frase = self.formarFrase(dic,verbos,fenomeno,grado)
            elif(self.forma == 1):
                verbos = grado.verbosDisminuir
                dic = grado.ordenarReversedGrado(grado.periodoGenerar,estadoPrecipitacion)
                frase = self.formarFrase(dic,verbos,fenomeno,grado)
               
        return frase
                
    def juntarFrase(self,lista):


        frase = ""
        
        i = 0
        for item in lista:
            
            if len(lista) > 1:
                if( i + 1 == len(lista)):
                    frase += " ,y " + item
                elif i != 0:
                    frase += ", " + item
                elif i==0:
                    frase +=  item
            else: frase += item
                 
        
            i += 1
            
        frase +="."
        return frase
            
    
    
        
    
                    