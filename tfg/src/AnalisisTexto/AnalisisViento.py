'''
Created on Mar 31, 2019

@author: rafaelsoriadiez
'''

import os
import spacy
import nltk
import numpy as np
import pandas as pd
from wordcloud import WordCloud

import matplotlib.pyplot as plt

def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/../textos/csv/crear/"
    nlp = spacy.load('es_core_news_md')
    
    colnames = ['provincia','fecha','frase','clase']
    total = pd.read_csv(path + "total.csv", names=colnames) 
   
    #viento

   
    
    datos = pd.DataFrame(total)
    viento = datos[datos['clase']== 'viento']
    viento = viento[viento['provincia']== 'TENERIFE']
    size = frecuenciaTemática(viento.frase)
    print("La cantiad de frases de viento en Tenerife es " + str(len(viento)))
    print("La longitud de viento en Tenerife es " + str(size))
    print("---------")
    
    
    datos = pd.DataFrame(total)
    viento = datos[datos['clase']== 'viento']
    viento = viento[viento['provincia']== 'ALACANT/ALICANTE']
    size = frecuenciaTemática(viento.frase)
    print("La cantiad de frases de viento en Alicante es " + str(len(viento)))
    print("La longitud de viento en Alicante es " + str(size))
    print("---------")
    
    datos = pd.DataFrame(total)
    viento = datos[datos['clase']== 'viento']
    viento = viento[viento['provincia']== 'LA RIOJA']
    size = frecuenciaTemática(viento.frase)
    print("La cantiad de frases de viento en LA RioJa es " + str(len(viento)))
    print("La longitud de viento en La RioJa es " + str(size))
    print("---------")
    
    datos = pd.DataFrame(total)
    viento = datos[datos['clase']== 'viento']
    viento = viento[viento['provincia']== 'MADRID']
    size = frecuenciaTemática(viento.frase)
    print("La cantiad de frases de viento en Madrid es " + str(len(viento)))
    print("La longitud de viento en Madrid es " + str(size))
    print("---------")
   
   
    datos = pd.DataFrame(total)
    viento = datos[datos['clase']== 'viento']    
    #buscarPalabras(viento.frase,nlp)
   # tokenizar(viento.frase,nlp)
    print("La longitud de frase de viento es: " + str(len(viento)))
    similitud('')
    
    

def frecuenciaTemática(frases):
    
    
    veces = 0
    size = 0
    
    for frase in frases:
        size += len(str(frase))
        veces += 1
        
        
    return size/veces
    

def buscarPalabras(frases,nlp):
    
    sumAumentar = 0
    sumDisminuir = 0
    sumClaros = 0
    sumNubosos = 0
    sumNoCambios = 0
    
    frases = np.array(frases)
    corpus = []
    doc = nlp(str(frases))
    #lo divido en frases
    newText = ""
    for token in doc:
        newText += token.lemma_ + " "
        if(token.text == '.'):
            corpus.append(newText)
        
    for frase in corpus:
       
        if "intervalo nuboso" in frase:
            sumNubosos += 1
        if "abrir claro" in frase:
            sumClaros += 1
        if "disminuir" in frase:
            sumDisminuir += 1
        if "aumentar" in frase:
            sumAumentar += 1
        if "sin cambio en la nubosidad" in frase:
            sumNoCambios += 1
            
        '''
        if(frase.find("intervalos nubosos") or frase.find("Intervalos nubosos")):
            sumNubosos += 1
        if(frase.find("disminuir") or frase.find("abrirse claros")):
            sumClaros += 1
        '''
            
            
    
    print("Intervalos nubosos " + str(sumNubosos))
    print("Abrirse claros " + str(sumClaros))
    print("Disminuir  " + str(sumDisminuir))
    print("Aumentar " + str(sumAumentar))
    print("sin cambio en la nubosidad " + str(sumNoCambios))
   
    

def tokenizar(frases,nlp):
    
    
    
    frases = np.array(frases)
    corpus = []
    corpusVerb=[]
    corpusSus=[]
    corpusAdj=[]
    corpusAdv=[]
    doc = nlp(str(frases))
    #lo divido en frases
    
    newText = ""
   
    for token in doc:
        if(token.pos_ == "NOUN"   or
          token.pos_ == "ADJ" or token.pos_ == "ADV"  or token.pos_ == "VERB"):
            print(token.text,token.lemma_)
            corpus.append(token.lemma_)
            newText += token.lemma_ + " "
        if(token.pos_ == "VERB"  ):
            corpusVerb.append(token.lemma_)
            
        elif(token.pos_ == "NOUN"):
            corpusSus.append(token.lemma_)
            
        elif(token.pos_ == "ADJ"):
            corpusAdj.append(token.lemma_)
            
        elif(token.pos_ == "ADV"):
            corpusAdv.append(token.lemma_)
            
    
    frecuencia(corpus)
    print("VERBOS")
    frecuencia(corpusVerb)
    print("SUSTANTIVOS")
    frecuencia(corpusSus)
    print("ADJETIVOS")
    frecuencia(corpusAdj)
    print("ADVERBIOS")
    frecuencia(corpusAdv)
    
    
    wordCloud(newText)
    #similitud(newText)
    
    
    

'''    


if(token1 != "norte" or token1 == "sur" or token1 == "este" or token1 =="oeste"
            or token1 == "nordeste" or token1 == "suroeste" or token1 == "noreste" or token1 == "sureste"):
            
'''
    
def similitud(newText):
  
    nlp = spacy.load('es_core_news_md')
    
    
    tokens = nlp('componente vertiente medianía') 
    
    
    for token1 in tokens:
        for token2 in tokens:
            print(token1.text, token2.text, token1.similarity(token2))
    
    
        
        
def frecuencia(corpus): 
    frecuencias = nltk.FreqDist(corpus)
    print(frecuencias)
    print(frecuencias.N)
    print(frecuencias.most_common(50))
    print("---------")
    
    

def wordCloud(corpus):
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(corpus)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    
    
    

main()