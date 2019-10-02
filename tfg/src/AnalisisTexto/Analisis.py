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
    
    
    colnames = ['provincia','fecha','frase','clase']
    total = pd.read_csv(path + "total.csv", names=colnames) 
   
    #temperatura
    datos = pd.DataFrame(total)
    temperatura = datos[datos['clase']== 'temperatura']    
    #tokenizarViento(temperatura.frase)
    print("La longitud de temperatura es: " + str(len(temperatura)))
    
    #Viento  
    datos = pd.DataFrame(total)
    viento = datos[datos['clase']== 'viento']    
    #tokenizarViento(viento.frase)
    print("La longitud de viento es: " + str(len(viento)))
    
    #nubes
    datos = pd.DataFrame(total)
    nubes = datos[datos['clase']== 'nubes']    
    #tokenizarViento(nubes.frase)
    print("La longitud de nubes es: " + str(len(nubes)))
    
    
    #precipitacion
    datos = pd.DataFrame(total)
    precipitacion = datos[datos['clase']== 'precipitacion']    
    #tokenizarViento(precipitacion.frase)
    print("La longitud de precipitacion es: " + str(len(precipitacion)))
    
    #nieve
    datos = pd.DataFrame(total)
    nieve = datos[datos['clase']== 'nieve']    
   # tokenizarViento(nieve.frase)
    print("La longitud de nieve es: " + str(len(nieve)))
    
    #humedad
    datos = pd.DataFrame(total)
    humedad = datos[datos['clase']== 'humedad']    
    tokenizarViento(humedad.frase)
    print("La longitud de humedad es: " + str(len(humedad)))

    
    
    
    

def tokenizar(frases):
    
    nlp = spacy.load('es_core_news_md')
    frases = np.array(frases)
    corpus = []
    

    doc = nlp(str(frases))
    #lo divido en frases
    
    newText = ""
   
    for token in doc:
        
        if((token.pos_ == "NOUN"  or token.pos_ == "VERB"  or
          token.pos_ == "ADJ" or token.pos_ == "ADV" )  and token.shape_ != "XXXX"):
            
            corpus.append(token.text)
            newText += token.text + " "
    
    
    frecuencia(corpus)
    
    wordCloud(newText)
    #similitud(newText)
    
# <bound method FreqDist.N of FreqDist({'flojo': 90, 'variable': 54, 'costa': 33, 'componente': 30, 'moderar': 23, 'brisa': 14, 'tender': 13, 'intervalo': 13, 'tardar': 11, 'fuerte': 9, ...})>


def tokenizarViento(frases):
    
    print(frases)
    nlp = spacy.load('es_core_news_md')
    frases = np.array(frases)
    corpus = []

    doc = nlp(str(frases))
    #lo divido en frases
    
    newText = ""
    print(frases)
    for token in doc:
        if(token.pos_ == "NOUN"  or token.pos_ == "VERB"  or
          token.pos_ == "ADJ" or token.pos_ == "ADV" ):
            print(token.text, token.lemma_,token.pos_)
            corpus.append(token.lemma_)
            newText += token.lemma_ + " "
    
    
    frecuencia(corpus)
    wordCloud(newText)
    #similitud(newText)
    
    
    
def esPuntoCardinal(token):
    
    if(token == "norte" or token == "sur" or token == "este" or token =="oeste"
            or token == "noroeste" or token == "suroeste" or token == "noreste" or token == "sureste"
            or token == "nordeste"):
        return True
    
    return False
    
    
'''    


if(token1 != "norte" or token1 == "sur" or token1 == "este" or token1 =="oeste"
            or token1 == "nordeste" or token1 == "suroeste" or token1 == "noreste" or token1 == "sureste"):
            
'''
    
def similitud(newText):
  
    nlp = spacy.load('es_core_news_md')
    tokens = nlp(newText) 
    
    puntosCardinales= ["norte","sur","este","oeste",
                       "noroeste","suroeste","noreste","sureste"]

    entrar1 = True
    entrar2 = True
    
    '''
    for token in tokens:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop)
    
    '''
    
    for token1 in tokens:
        for token2 in tokens:
            if(token1.similarity(token2) >= 1 and  token1.text != token2):
                print(token1.text, token2.text, token1.similarity(token2))
    
        
        
def frecuencia(corpus): 
    frecuencias = nltk.FreqDist(corpus)
    print(frecuencias)
    print(frecuencias.N)
    print(frecuencias.most_common(50))
    
    

def wordCloud(corpus):
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(corpus)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    
    
    

main()