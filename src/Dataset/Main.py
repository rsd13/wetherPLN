'''
Created on Nov 17, 2018

@author: rafaelsoriadiez
'''

#from ..BBDD.Provincia import Localidad

import requests
import json
import os
from src.BBDD.BDLocalidad import BDLocalidad
from src.Dataset.Fecha import Fecha
from src.BBDD.BDFecha import BDFecha
from src.Dataset.Hora import Hora
from src.BBDD.BDHora import BDHora
from src.BBDD.BDProvincia import BDProvincia
from src.BBDD.BDTextoProvincia import BDTextoProvincia
from os.path import join, dirname
from dotenv import load_dotenv

#parte de codigo para reecoger las keys
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
client_id = os.environ.get("SECRET")

fechaGlobal = ""

def conexion(codigo):

    url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/" + codigo + "/"
    #codigo de api
    querystring = {"api_key":client_id}
    headers = {
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    #lo transformo el un diccionario
    dic = json.loads(response.text)
    #recojo la url con los datos
    urldatos = dic["datos"]
    response = requests.get(urldatos)
    #recojo los datos que quiero y los guardo en un diccionario
    dic = json.loads(response.text)
    return dic



#hago 24 horas e introduzco la fecha
def crearListas(predicion,fecha,codigoProncia,codigoLocalidad):
    lista = []
    for i in predicion:
        hora = Hora()
        hora.fecha = fecha
        hora.codLocalidad = codigoProncia
        hora.codProvincia = codigoLocalidad
        lista.append(hora)
    
    return lista
  

#introduzco la fecha en la bbdd
def createFecha(fechaHoy):

    print("La fecha es: " + fechaHoy)
    fechaHoy = fechaHoy.split("-")
    año = fechaHoy[0]
    mes = fechaHoy[1]
    dia = fechaHoy[2]
    fechaHoy = Fecha(dia,mes,año)
    bdFecha = BDFecha()
    bdFecha.insertFecha(fechaHoy)
    global fechaGlobal
    fechaGlobal = fechaHoy
    return fechaHoy


def inDatos(codigoProvincia,codigoLocalidad):
    
    dic = conexion(codigoProvincia + codigoLocalidad)
    
    prediccion = dic[0]["prediccion"]["dia"][1]
    
    fechaHoy = prediccion["fecha"]
    #conseguimos la fecha
    fechaHoy = createFecha(fechaHoy)
    #recojo todos los datos
    estadoCielo = prediccion["estadoCielo"]
    precipitacion = prediccion["precipitacion"]
    nieve =  prediccion["nieve"]
    temperatura = prediccion["temperatura"]
    sensTermica = prediccion["sensTermica"]
    humedadRelativa = prediccion["humedadRelativa"]
    viento = prediccion["vientoAndRachaMax"]
    probTormenta = prediccion["probTormenta"]
    probPrecipitacion = prediccion["probPrecipitacion"]
    probNieve = prediccion["probNieve"]
    
    #creo 24 objetos Hora, 1 por hora
    listaHoras = crearListas(estadoCielo,fechaHoy,codigoProvincia,codigoLocalidad)
    #introducirDatos(estadoCielo,listaHoras)
    i = 0
    while i < len(estadoCielo):
        listaHoras[i].introducirEstadoCielo(estadoCielo[i],listaHoras[i])
        listaHoras[i].introducirPrecipitacion(precipitacion[i],listaHoras[i])
        listaHoras[i].introducirNieve(nieve[i],listaHoras[i])
        listaHoras[i].introducirTemperatura(temperatura[i],listaHoras[i])
        listaHoras[i].introducirSensTermica(sensTermica[i],listaHoras[i])
        listaHoras[i].introducirHumedad(humedadRelativa[i],listaHoras[i])
        i = i + 1

    i = 0
    j = 0
    #tiene el doble tamaño porq estan junto viento y racha
    while i < len(viento):
        listaHoras[j].introducirViento(viento[i],listaHoras[j])
        i = i + 1
        listaHoras[j].introducirRacha(viento[i],listaHoras[j])
        i = i + 1
        j = j + 1
        
    i = 0
    j = 0
    contador = 0
    while i < len(estadoCielo):
        #cogemos el primer valor
        
        #6 veces, porque lo contiene n un rango de 6 horas
        if(contador == 6):
            j += 1
            contador = 0
            
        listaHoras[i].introducirProbTormenta(probTormenta[j],listaHoras[i])
        listaHoras[i].introducirProbPrecipitacion(probTormenta[j],listaHoras[i])
        listaHoras[i].introducirProbNieve(probTormenta[j],listaHoras[i])
        contador += 1     
        i = i + 1
    
    insertarHora(listaHoras)


def insertarHora(horas):
    bdHora = BDHora()
    for hora in horas:
        bdHora.insertHora(hora)
        
        
def conexionTexto(codigoComunidad,codigoProvincia):
    
    url = "https://opendata.aemet.es/opendata/api/prediccion/provincia/manana/" + codigoProvincia + "/"
    #codigo de api
    querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJyc29yaWFkaWV6QGdtYWlsLmNvbSIsImp0aSI6IjI4NDM3MjU5LTkwYTUtNDg4ZS1hOTJkLTFlYzk0MDE1ZjA4MCIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTQxMTcyMzM4LCJ1c2VySWQiOiIyODQzNzI1OS05MGE1LTQ4OGUtYTkyZC0xZWM5NDAxNWYwODAiLCJyb2xlIjoiIn0.5RAD-t1Jm0xwq-XzcsuWAXfc1H0qgqOUgWx-ykfsMII"}
    headers = {
       'cache-control': "no-cache"
       }
    response = requests.request("GET", url, headers=headers, params=querystring)
    #lo transformo el un diccionario
    dic = json.loads(response.text)

    #recojo la url con los datos
    urldatos = dic["datos"]
    print(urldatos)
    response = requests.get(urldatos)
    #me guardo el texto
    return response.text
        
        
def inDatosTexto(codigoComunidad,codigoProvincia):
    texto = conexionTexto(codigoComunidad,codigoProvincia)
    textoProvincia = BDTextoProvincia()
    textoProvincia.insertTexto(fechaGlobal, codigoProvincia, codigoComunidad, texto)
    #creamos el fichero
    fecha = fechaGlobal.dia + "-" + fechaGlobal.mes + "-"+fechaGlobal.año
    dir_path = os.path.dirname(os.path.abspath(__file__))
    if(codigoComunidad == "mad"):
        fichero = open(dir_path +"/../textos/madrid/" +  fecha + ".txt","w")
    elif(codigoComunidad == "coo"):
        fichero = open(dir_path +"/../textos/canarias/" +  fecha + ".txt","w")
    elif(codigoComunidad == "rio"):
        fichero = open(dir_path +"/../textos/rioja/" +  fecha + ".txt","w")
    elif(codigoComunidad == "val"):
        fichero = open(dir_path +"/../textos/alicante/" +  fecha + ".txt","w")
        
    fichero.write(texto)
    fichero.close()
    
def recogidaDatos():
    localidad = BDLocalidad()
    lineas = localidad.selectAll()
    
    #voy hacerlo con 1 de prueba
    codigo = lineas[0]['codprovincia'] + lineas[0]['codigo']
   
    
    for linea in lineas:
        inDatos(linea['codprovincia'],linea['codigo']) 
    
    #una vez obtenido los datos, vamos a buscar su texto correspondiente
    provincia = BDProvincia()
    lineas = provincia.selectAll()
    
    for linea in lineas:
        inDatosTexto(linea['codComunidad'],linea['codigo']) 
    
    
recogidaDatos()
