
import sqlite3
import os
from src.Dataset.Hora import Hora
from llvmlite.tests.test_binding import asm_inlineasm
class BDHora:

#hora,dai,mes,año,estadoCielo,precipitacion,probPreci,probTormenta,nieve,probNieve
#temperatura,sensTeermica,humedadRelativa,velocidadV,rachaMax,direcionViento,codLocalidad
#codProvincia
    def __init__(self):
        #ruta de la base de datos
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        self.bbdd = sqlite3.connect(dir_path + "/Weather.db",timeout=10)
        self.bbdd.row_factory = sqlite3.Row
        self.cursor = self.bbdd.cursor()
        
    
    #TIENES QUE REVISAR LOS TIEMPOS RELACIONADOS CON EL VOIENTO
    def insertHora(self,hora):
        #comprobamos si existe
        self.cursor.execute("select * " + 
                            "from hora " +
                            "where hora=? and dia=? and mes=? and año=? and codProvincia=?" +
                            " and codLocalidad=?",(
                            hora.hora,
                            hora.fecha.dia,
                            hora.fecha.mes,
                            hora.fecha.año,
                            hora.codProvincia,
                            hora.codLocalidad))
         
        lineas = self.cursor.fetchall()
        
        #si no existe esa fecha se inserta 
        if len(lineas) == 0:
            self.cursor.execute("INSERT INTO hora VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(
                hora.hora,
                hora.fecha.dia,
                hora.fecha.mes,
                hora.fecha.año,
                hora.estadoCielo,
                hora.precipitacion,
                hora.probPrecipitacion,
                hora.probTormenta,
                hora.nieve,
                hora.probNieve,
                hora.temperatura,
                hora.sensTermica,
                hora.humedadRelativa,
                hora.velocidadViento,
                hora.direccionViento,
                hora.rachaMax,
                hora.codLocalidad,
                hora.codProvincia))
             
            self.bbdd.commit()
            
            
      
    def getCodProvincia(self,ciudad):      
        if(ciudad == "ALACANT/ALICANTE"): ciudad = "Alicante/Alacant"
        if(ciudad == "TENERIFE"): ciudad = "Santa Cruz de Tenerife"

        self.cursor.execute("Select codigo FROM Provincia where nombre like ?",(
            ciudad,))
        
        lineas = self.cursor.fetchall()
        
        return lineas[0][0]
        
    def getNube(self,ciudad,fecha):
        
        fechas = fecha.split("-")
        
        anyo = fechas[0]
        mes = fechas[1]
        dia = fechas[2]
        
        codProvincia = self.getCodProvincia(ciudad)
       
        self.cursor.execute("Select hora, estadoCielo FROM hora where  dia=? and mes=? and año=? and codProvincia = ?",(
            dia,
            mes,
            anyo,
            codProvincia))
            
        
        lineas = self.cursor.fetchall()
        
        dicci ={}
        list = []
        sum = 0
        for linea in lineas: 
            
            
            hora = linea[0]
            estado = linea[1]
           
           
            dicci[hora] = estado
            #list.append(datos)
            
            sum+=  1
           
            if(sum == 24):
                list.append(dicci)
                sum = 0
                dicci ={}
            
            
       
        return list
    
    
    def getViento(self,ciudad,fecha):
        
        fechas = fecha.split("-")
        anyo = fechas[0]
        mes = fechas[1]
        dia = fechas[2]
        
        codProvincia = self.getCodProvincia(ciudad)
       
        self.cursor.execute("Select hora, velocidadViento, direccionViento, rachaMax" + 
                            " FROM hora where  dia=? and mes=? and año=? and codProvincia = ?",(
            dia,
            mes,
            anyo,
            codProvincia))
            
        
        lineas = self.cursor.fetchall()
        
        dicVelocidad ={}
        dicDirecion = {}
        dicRacha = {}
        
        listTotal = []
        listPrecipitacion = []
        listProbPrecipitacion = []
        listProbTormenta = []
        sum = 0
        for linea in lineas: 
            
            
            hora = linea[0]
            velocidad = linea[1]
            direcion = linea[2]
            racha = linea[3]
           
            dicVelocidad[hora] = velocidad
            dicDirecion[hora] = direcion
            dicRacha[hora] = racha
            
            
            sum+=  1
           
            if(sum == 24):
                listPrecipitacion.append(dicVelocidad)
                listProbPrecipitacion.append(dicDirecion)
                listProbTormenta.append(dicRacha)
                sum = 0
                dicVelocidad ={}
                dicDirecion = {}
                dicRacha = {}
            
        
        listTotal.append(listPrecipitacion)  
        listTotal.append(listProbPrecipitacion)  
        listTotal.append(listProbTormenta)  
        return listTotal
    
    
    
    
    def getPrecipitacion(self,ciudad,fecha):
        
        fechas = fecha.split("-")
        anyo = fechas[0]
        mes = fechas[1]
        dia = fechas[2]
        
        codProvincia = self.getCodProvincia(ciudad)
       
        self.cursor.execute("Select hora, precipitacion, probPrecipitacion, probTormenta, nieve, probNieve" + 
                            " FROM hora where  dia=? and mes=? and año=? and codProvincia = ?",(
            dia,
            mes,
            anyo,
            codProvincia))
            
        
        lineas = self.cursor.fetchall()
        
        dicPrecipitacion ={}
        dicProbPrecipitacion = {}
        dictProbTormenta = {}
        dicNieve = {}
        dicProbNieve = {}
        
        listTotal = []
        listPrecipitacion = []
        listProbPrecipitacion = []
        listProbTormenta = []
        listNieve = []
        listProbNieve = []
        sum = 0
        for linea in lineas: 
            
            
            hora = linea[0]
            precipitacion = linea[1]
            probPrecipitacion = linea[2]
            probTormenta = linea[3]
            nieve = linea[4]
            probNieve = linea[5]
           
            dicPrecipitacion[hora] = precipitacion
            dicProbPrecipitacion[hora] = probPrecipitacion
            dictProbTormenta[hora] = probTormenta
            dicNieve[hora] = nieve
            dicProbNieve[hora] = probNieve
            
            
            sum+=  1
           
            if(sum == 24):
                listPrecipitacion.append(dicPrecipitacion)
                listProbPrecipitacion.append(dicProbPrecipitacion)
                listProbTormenta.append(dictProbTormenta)
                listNieve.append(dicNieve)
                listProbNieve.append(dicProbNieve)
               
                sum = 0
                dicPrecipitacion ={}
                dicProbPrecipitacion = {}
                dictProbTormenta = {}
                dicNieve = {}
                dicProbNieve = {}
            
        
        listTotal.append(listPrecipitacion)  
        listTotal.append(listProbPrecipitacion)  
        listTotal.append(listProbTormenta)  
        listTotal.append(listNieve)  
        listTotal.append(listProbNieve)  
        return listTotal
         
         

    
    def getCiudades(self,codProvincia):

        self.cursor.execute("SELECT codigo,nombre" + 
                            " FROM LOCALIDAD " + 
                            " WHERE  codprovincia= "+ codProvincia)
            
        
        rows = self.cursor.fetchall()
        
        ciudades = []
        
        for row in rows:
            
            item = (row[0],row[1])
            ciudades.append(item)
        
        return ciudades
        
         
    def getTemperatura(self,provincia,fecha,esMayor):
        fechas = fecha.split("-")
        anyo = fechas[0]
        mes = fechas[1]
        dia = fechas[2]
        
        result = []
        dicHora ={}
        codProvincia = self.getCodProvincia(provincia)
        ciudades = self.getCiudades(codProvincia)
        lista = []
        for ciudad in ciudades:
            codLocalidad = ciudad[0]
            nombre = ciudad[1]
          
            self.cursor.execute(" SELECT temperatura,hora " + 
                            " FROM Hora,localidad " + 
                            " WHERE hora.codProvincia = localidad.codProvincia and hora.codLocalidad = localidad.codigo " +
                            " and localidad.codigo=? and localidad.codProvincia =? " + 
                            " and dia=? and mes=? and año=?",(
            codLocalidad,
            codProvincia,
            dia,
            mes,
            anyo))
            
            dic = {}
            dicHora ={}
            
            temperatura = []
            rows = self.cursor.fetchall()
            mayor = -999
            menor = 999
            for row in rows:
                if esMayor:
                  
                  
                    dato = int(row[0])
                  
                    if dato > mayor:
                        mayor = dato
                    if dato < menor:
                        menor = dato
                    
                    
                else:
                    lista.append(row[0])

           
            
            if esMayor:
                result.append(nombre +":" + str(mayor) + ":" + str(menor))
            else:
                
                result = lista
          
        
            
            
        
        
        return result
                
                
                
                
            
            
            
        
        
         
            


                            