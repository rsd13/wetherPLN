'''
Created on Dec 28, 2018

@author: rafaelsoriadiez
'''




import os
import spacy

def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    
    
    pathAlicante = dir_path + "/../textos/alicante/"
    pathCanarias = dir_path +"/../textos/canarias/"
    pathMadrid = dir_path + "/../textos/madrid/";
    pathrioja = dir_path + "/../textos/rioja/";
    '''
    nb = input('¿Quieres entrenamiento, test o ambos?: (0/entrenamiento,1/test,2/ambos): ' )
    if(nb == "0"):
        entrenamiento(pathAlicante)
        entrenamiento(pathMadrid)
    elif(nb == "1"): 
        test(pathCanarias)
        test(pathrioja)
    elif(nb=="2"):
        entrenamiento(pathAlicante)
        entrenamiento(pathMadrid)
        test(pathCanarias)
        test(pathrioja)'''
    
    normal(pathAlicante)
    normal(pathCanarias)
    normal(pathMadrid)
    normal(pathrioja)
    
def entrenamiento(cadena):
    corpus = []
    
    
    
    for fichero in os.listdir(cadena):
        if fichero.find(".txt") >= 0:
            dir_path = cadena + fichero
            file = open(dir_path,"r")
            texto = file.read()
            tokenizar(texto,corpus)
   
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/textos/csv/crear/"
    ficheroCSV = open (path + "entrenamiento.csv", "a")
    
    ficheroCSV.write("frase,clase\n")
    
    for frase in corpus:
        ficheroCSV.write(frase + ",\n")
         
def test(cadena):
    corpus = []

    for fichero in os.listdir(cadena):
        if fichero.find(".txt") >= 0:
            dir_path = cadena + fichero
            file = open(dir_path,"r")
            texto = file.read()
            tokenizar(texto,corpus)
            
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/textos/csv/crear/"
    ficheroCSV = open (path + "test.csv", "a")
    
    ficheroCSV.write("frase,clase\n")
    
    for frase in corpus:
        ficheroCSV.write(frase + ",\n")

''' quito el ruido, ya que, todos los textos a partir de la linea 13 tiene la zona del contenido '''
def normalizarTexto(texto):
    
    contador = 1
    i = 0
    aux = 1
    newText = ""
    while (i < len(texto)):
        if(texto[i] == "\n"): contador +=1
        if(contador >= 13):
            if (texto[i] == "\n"):
                if(aux == 0):
                    space = ' '
                    newText += space
                if(aux == 1):
                    space = ''
                    newText += space
                aux = 1
              
            else:
                newText += texto[i]
                aux = 0
            
        i += 1
    
    
    return newText

def normal(cadena):
    corpus = []

    for fichero in os.listdir(cadena):
        if fichero.find(".txt") >= 0:
            dir_path = cadena + fichero
            file = open(dir_path,"r")
            texto = file.read()
            texto = normalizarTexto(texto)
            tokenizar(texto,corpus)
               

    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/textos/csv/crear/"
    ficheroCSV = open (path + "normal.csv", "a")
    
    ficheroCSV.write("frase,clase\n")
    
    for frase in corpus:
        ficheroCSV.write(str(frase) + ",\n")
    

def tokenizarN(texto,corpus):
    newText = ''
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(texto)
    #lo divido en frases
    sents = list(doc.sents)
    
    for sent in sents:
        corpus.append(sent)
        
    
    corpus.pop()

def tokenizar(texto,corpus):
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(texto)
    #lo divido en frases
    sents = list(doc.sents)
    newText = ""
    for sent in sents: 
        for token in sent:
        
            if((token.pos_ == "NOUN"  or token.pos_ == "VERB"  or
              token.pos_ == "ADJ")  and token.shape_ != "XXXX"):
                #print(token)
                newText = newText + " " + str(token)
                #print(token.text,": " ,token.pos_,token.tag_,token.lemma_)
        
        #no se introduce          
        if(newText != ''):
            corpus.append(newText)
        newText = ""
    return newText

    
main()