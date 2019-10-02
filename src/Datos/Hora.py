'''
Created on Mar 29, 2019

@author: rafaelsoriadiez
'''


class Hora:
    
    def __init__(self):
        self.madrugada = []
        self.mañana = []
        self.central = []
        self.tarde = []
        self.noche =[]
        self.total = []
        
        
        
    def splitDia(self,lista):
       
        dicMadrugada ={}
        dicMañana ={}
        dicCentral ={}
        dicTarde ={}
        dicNoche ={}
        dicTotal ={}
        
        for dic in lista:
            for hora, dato in dic.items():
                dicTotal[hora] = dato
                if( hora >= "08" and hora <= "19"):  
                    if(hora >= "08" and hora <="12"):
                        dicMañana[hora] = dato
                    
                    if(hora >= "10" and hora <="14"):
                        dicCentral[hora] = dato
                        
                    if (hora >="13" and hora <="19"):
                       dicTarde[hora] = dato
                
                if(hora >= "20" and hora <= "23"):
                    dicNoche[hora] = dato
                    
                if(hora >= "00" and hora <= "07"):
                   dicMadrugada[hora] = dato
               
            self.mañana.append(dicMañana)  
            self.central.append(dicCentral)  
            self.tarde.append(dicTarde)  
            self.noche.append(dicNoche)  
            self.madrugada.append(dicMadrugada)
            self.total.append(dicTotal)
           
          
    

            
    
  
