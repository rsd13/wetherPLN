import os
import spacy
from src.AnalisisTexto.SVM import main as svm




from datetime import datetime, timedelta

meses = {'ENERO' : '01',
         'FEBRERO' : '02',
         'MARZO' : '03',
         'ABRIL' : '04',
         'MAYO' : '05',
         'JUNIO' : '06',
         'JULIO' : '07',
         'AGOSTO' : '08',
         'SEPTIEMBRE' : '09',
         'OCTUBRE' : '10',
         'NOVIEMBRE' : '11',
         'DICIEMBRE' : '12',}

def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    
    
    pathAlicante = dir_path + "/../textos/alicante/"
    pathCanarias = dir_path +"/../textos/canarias/"
    pathMadrid = dir_path + "/../textos/madrid/";
    pathrioja = dir_path + "/../textos/rioja/";
    
    getText(pathAlicante)
    getText(pathCanarias)
    getText(pathMadrid)
    getText(pathrioja)
    


def cleanText(texto):
    
    salir = "TEMPERATURAS MÍNIMAS Y MÁXIMAS PREVISTAS (C):"
    newText = ''

    for item in texto[12:]:
        if item == salir: break
        elif str(item) != '': newText += item 
        elif str(item) == '': newText += " " 
        elif str(item) == ",": newText += ";" 
       
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(newText)
    newText = ""
    for token in doc:   
        if(token.text == ","):  newText += ";"
        elif(token.pos_ == "SPACE"):  pass
        else: newText += token.text + " "
        
    return newText
   
    
    
   
def splitSents(texto):
    
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(texto)
    #lo divido en frases
    sents = list(doc.sents)
    
    return sents
   
    
def getFecha(texto):
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(texto)
    year = mes = dia = ''
    
    #I look if token is day, year or month
    for token in doc:
       
        if(token.pos_ == "NUM" and token.shape_ != 'dd:dd'):
            if( token.shape_ == 'd'):  dia = '0' + str(token)
            elif (token.shape_ == 'dd'): dia = token
            elif (token.shape_ == 'dddd'): year = token
        
        if meses.get(str(token)):
            mes = meses[str(token)]
    
    
    #
    fecha = str(year) + "/" + str(mes) + "/" + str(dia)
    date = datetime.strptime(fecha, "%Y/%m/%d")
    modified_date = date + timedelta(days=1)
    modified_date = str(modified_date).split(" ")
    fecha =  modified_date[0]


    return fecha

       

    
   
def getText(cadena):
    corpus = []
    provincia = ''
    fecha = ''
    newText = '' 
    
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/../textos/csv/crear/"
    ficheroCSV = open (path + "total.csv", "a")
    
    ficheroCSV.write("provincia,fecha,frase,clase\n")
   
    clasificador = svm()
    
   
    
    for fichero in os.listdir(cadena):
        if fichero.find(".txt") >= 0:
            dir_path = cadena + fichero
            file = open(dir_path,"r")
            texto = file.read().splitlines()
            
            provincia = texto[10]
            fecha = texto[4]
            print(fecha)
            fecha = getFecha(fecha)
           
            newText = cleanText(texto)
            corpus = splitSents(newText)
            
            
            
            for frase in corpus:
                clase = clasificador.predict([str(frase)])
                print(fecha)
            
                ficheroCSV.write(str(provincia) +  "," + str(fecha) + 
                                 ","  + str(frase) + "," + str(clase[0]) +  "\n")
                
                
                
                


                
main()
   
   

        