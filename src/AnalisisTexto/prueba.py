import os
import spacy
import pandas as pd
import numpy as np
import nltk
from src.Weather.SVM import main as svm

sumNubes = 0
sumViento = 0
sumTemperatura = 0
sumPrecipitacion = 0
sumNieve = 0
sumHumedad = 0

def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    
    path = dir_path + "/../textos/csv/crear/"
    pathAlicante = dir_path + "/../textos/alicante/"
    pathCanarias = dir_path +"/../textos/canarias/"
    pathMadrid = dir_path + "/../textos/madrid/";
    pathrioja = dir_path + "/../textos/rioja/";
    nlp = spacy.load('es_core_news_sm')
    
    
    
    promedioLogintud(pathAlicante,nlp)
    imprimir("Alicante")
    print("Cantidad de temática nube en Alicante " + str(sumNubes))
    print("Cantidad de temática viento en Alicante " + str(sumViento))
    print("Cantidad de temática temperatura en Alicante " + str(sumTemperatura))
    print("Cantidad de temática precipitacion en Alicante " + str(sumPrecipitacion))
    print("Cantidad de temática nieve en Alicante " + str(sumNieve))
    print("Cantidad de temática humedad en Alicante " + str(sumHumedad))
    
    #promedioLogintud(cadena,nlp):
    #promedioLogintud(cadena,nlp):
    #promedioLogintud(cadena,nlp):

    
def imprimir(ciudad):
    print("Cantidad de temática nube en" + ciudad +  str(sumNubes))
    print("Cantidad de temática nube en" + ciudad +  str(sumViento))
    print("Cantidad de temática nube en" + ciudad +  str(sumNubes))
    print("Cantidad de temática nube en" + ciudad +  str(sumNubes))
    print("Cantidad de temática nube en" + ciudad +  str(sumNubes))
    print("Cantidad de temática nube en" + ciudad +  str(sumNubes))
    
def cleanText(texto,nlp):
    
    salir = "TEMPERATURAS MÍNIMAS Y MÁXIMAS PREVISTAS (C):"
    newText = ''

    for item in texto[12:]:
        if item == salir: break
        elif str(item) != '': newText += item 
        elif str(item) == '': newText += " " 
        elif str(item) == ",": newText += ";" 
       
    
    doc = nlp(newText)
    newText = ""
    for token in doc:   
        if(token.text == ","):  newText += ";"
        elif(token.pos_ == "SPACE"):  pass
        else: newText += token.text + " "
        
    return newText
   

def temáticas(text,clasificador,nlp):
    doc = nlp(text)

    sents = list(doc.sents)
    lista = []
    
    global sumNubes 
    global sumViento 
    global sumTemperatura 
    global sumPrecipitacion 
    global sumNieve 
    global sumHumedad 
    
    for frase in sents:
        clase = clasificador.predict([str(frase)])
        clase = clase[0]
        if clase == "nubes": 
            sumNubes += 1
        elif clase == "viento": 
            sumViento +=1
        elif clase == "temperatura": 
            sumTemperatura +=1
        elif clase == "precipitacion": 
            sumPrecipitacion += 1
        elif clase == "nubes-precipitacion":
            sumNubes += 1
            sumPrecipitacion += 1
        elif clase == "nieve":
            sumNieve +=1
        elif clase == "humedad":
            sumHumedad +=1
        
    
   
    
    
            
            
    

def promedioLogintud(cadena,nlp):
    
    
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/textos/csv/crear/"
    clasificador = svm()
    
    ficheros = 0
    longitud = 0
    
    global sumNubes 
    global sumViento 
    global sumTemperatura 
    global sumPrecipitacion 
    global sumNieve 
    global sumHumedad 
    
    sumNubes = 0
    sumViento = 0
    sumTemperatura = 0
    sumPrecipitacion = 0
    sumNieve = 0
    sumHumedad = 0
    
    for fichero in os.listdir(cadena):
        if fichero.find(".txt") >= 0:
            dir_path = cadena + fichero
            file = open(dir_path,"r")
            texto = file.read().splitlines()
            newTexto = cleanText(texto,nlp)
            temáticas(newTexto,clasificador,nlp)
            longitud =+ len(newTexto)
            ficheros =+ 1
           
            
    
    
    print("La longitud es " + str(longitud/ficheros))
    
    
    
    return longitud/ficheros

    

    




main ()