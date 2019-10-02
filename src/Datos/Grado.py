'''
Created on Apr 10, 2019

@author: rafaelsoriadiez
'''


#VERBOS
verbosDisminuir = [
    "que remiten","que disminuyen",
    "que desaparecen", "que se aislan",
    "que disipan" ]


verbosAumentar = [
    "que crecen","que aumentan",
    "que se abren",
    "que se intesifican","que se extienden"
]


verbosGeneral = [
    "que predominan",
    "que se esperan", "que afectan"
]

adverbiosGeneral = [
    "principalmente", "mayoritariamente",
    "primordialmente"
]


#ADJETIVOS

adjetivosCambios = [
    "notable","extraordinario",
    "fuerte","intenso","alto",    
]


adjetivosCambios = [
    "notable","extraordinario",
    "fuerte","intenso","alto",    
]



import random

   
   



class Grado:
    def __init__(self):
        self.periodoGenerarIgual = {}
        self.periodoMejor = {}
        self.periodoMayor = {}
        self.periodoGenerar = []
        self.periodoLluvias = {}
        #Periodo y grado
        self.mayor = ''
        self.menor = ''
        
        self.verbosDisminuir= verbosDisminuir
        self.verbosAumentar= verbosAumentar
        self.verbosGeneral= verbosGeneral
        self.adverbiosGeneral= adverbiosGeneral
        
    #Devuelve el periodo total
    def mirarPeriodo(self,periodo):
        frase = ''
        dia = False
        madrugada = mañana = central = tarde = noche = False
       
        for item in periodo:
            if item == "madrugada" : madrugada = True
            if item == "mañana":  mañana = True
            if item == "horas centrales de la " :  central = True
            if item == "tarde" :  tarde = True
            if item =="noche" :  noche = True
        
        if madrugada and mañana and central and tarde and noche:
            frase += "durante todo el día,"
            madrugada = mañana = central = tarde = noche = False
        
        if madrugada and mañana and central: 
            frase += "durante la primera mitad del día,"
            madrugada = mañana = central  = False
            
        if mañana and central and tarde: 
            frase += "por el día,"
            mañana = central = tarde  = False
        
        if central and tarde and noche: 
            frase += "durante la segunda mitad del día,"
            central = tarde = noche  = False
            
        
        listaPrep = ["durante " ,"por "]
        if madrugada: frase +=  random.choice(listaPrep) + "la madrugada,"
        if mañana: frase += "durante la mañana,"
        if central: frase += "en las horas centrales del día,"
        if tarde: frase += random.choice(listaPrep)+ "la tarde,"
        if noche: frase +=  random.choice(listaPrep) + "la noche,"
            
        lista = frase.split(",")
        lista.pop()
        
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
    
   
    def analizarPeriodos(self,estado,periodoTemporal,estadoNext,periodoTemporalNext,size):
        
        gradoNubes = Grado()
        i = 0
        igual = False
        listaIgual = []
        verbo = resultIgual = ''
      
        while i < size:
           
            result = ''
            
            
            #Miro si sube o baja o si es igual
            grados = self.mirarNivelGrado(estado,estadoNext)
                
            #Si es el último (noche) me da igual
            if i+1 == size:
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
                print(resultIgual)
                resultIgual += ":" + verbo
                igual = False 
                result = resultIgual
                listaIgual = []
            else: result = periodoTemproral + ":" + estado + ":" + verbo
            gradoNubes.periodoGenerar.append(result)
            
            i += 1
           
   


    
    def ordenarReversedGrado(self,diccionario,estadoFenomeno):
        dic = {}
        
        for estado in reversed(estadoFenomeno):
            
            if estado in diccionario:
                dic[estado] = diccionario[estado]
                
        return dic
    
    def ordenarGrado(self,diccionario,estadoFenomeno):
        dic = {}
        
        for estado in estadoFenomeno:
            if estado in diccionario:
                dic[estado] = diccionario[estado]
                
        return dic
   
                
        
        
    
    
    
        