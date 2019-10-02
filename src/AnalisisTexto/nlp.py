'''
Created on Nov 30, 2018

@author: rafaelsoriadiez
'''
'''
Created on Nov 29, 2018

@author: rafaelsoriadiez
'''
import nltk
import re
import os
import spacy
from spacy.lang.es.examples import sentences
from math import sin #para usar la función seno
from time import time #importamos la función time para capturar tiempos
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


tenerife = re.compile("Santa Cruz de Tenerife")


def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    fecha = "20-11-2018"
    
    fichero = open(dir_path +"/../textos/canarias/" +  fecha + ".txt","r")
    #obtengo el texto del fichero 
    texto = fichero.read()
    print(texto[0])
    contador = 1
    i = 0
    salir = 0
    newText = ""
    while (i < len(texto) and salir == 0):
        if(texto[i] == "\n"): contador +=1
        print(contador)
        if(contador >= 13):
            newText += texto[i]
        
        i += 1
    
    print("----")
    print(newText)
    #bagWords(texto)
    #similitud()
    tonekizarSpacy(texto)
    #tokenizarTree(texto)
    #okenización del texto
    #dividir el texto en parque mas pequeñas
    #tokenizar(texto)
    #postagger(texto)
    
    
    

# https://spacy.io/usage/linguistic-features#tokenization 


'''
metodos: 

    - text: devuelve las parabras
    - lemma_: la forma base de la palabra
    - pos_ : que es cada palabra (nombre, etc...)
    - tag: etiquetas detallada si el verbo esta en pasado, por ejemplo
    - dep: analisis sintáctico https://spacy.io/api/annotation
    - shape_: la forma de la palabra (te dice si va en mayus o minus)
    - is_alpha: booleano que te dice si es alga 
    - is_stop: booleano que te dice si la palabra es común  (no funciona bn en castellano)
    -----------------------------
    NOUM CHUNKS: define al sustantov, es decir: the lavish green grass,
    define que la hierba es verde.
'''
    
def tonekizarSpacy(texto):
    #renonecedor de entidades
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(texto)
    
    print("numeros de caracteres: " + str (len(doc)))
    
    for token in doc: 
        #token.tex lo tokeniza en palabras
        
        if(token.shape_ != "XXXX"):
            print(token.text,": " ,token.pos_,token.tag_,token.shape_)
        #print("-----")
        
        
        #print(token.text, token.pos_, token.dep_)
    

    print("-------------------------------")
    for chunk in doc.noun_chunks:
        print(chunk.text)
    
   
    print("---------------------")
    print("---------------------")
    print("---------------------")
    i = 1
    for sent in doc.sents:
        print("frase: " , i ,sent.text)
        i+=1
    
       


''' 
 Navigating the parse tree
    heald and child describle palabras conectadas en un arco del arbol de dependecias  
    
    - .n_rights: nos dicel el número de hijos que hay por la derecha
    - n_lefts: lo mismo con la izquierda
'''   


# https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction 
def bagWords(texto):
    corpus = [
        'All my cats in a row',
        'When my cat sits down, she looks like a Furby toy!',
        'The cat from outer space',
        'Sunshine loves to sit like this for some reason.'
    ]
   
    
    vectorizer = CountVectorizer()
    
    print( vectorizer.fit_transform(corpus).todense() )
    print( vectorizer.vocabulary_ )
    
    
    
    
    
   
 
def tokenizarTree(texto):
    nlp = spacy.load('es_core_news_md')
    doc = nlp(texto)
    
    
    for token in doc:
        #token.tex lo tokeniza en palabras
        
        print(token.text,
          [child for child in token.children])
    
    
    print("-------")
    print([token.text for token in doc[0].rights])
    print(doc[2].n_rights)  # 1
    
   
# https://spacy.io/usage/vectors-similarity

def similitud():
    tiempo_inicial = time() 
    nlp = spacy.load('es_core_news_md')
    tiempo_final = time() 
    tokens = nlp('precipitación lluvia nube tormenta cielo perro animal') 
    
    
    for token1 in tokens:
        for token2 in tokens:
            print(token1.text, token2.text, token1.similarity(token2))
    
    
    
    
    print("El tiempo es " + str(tiempo_final - tiempo_inicial))

def tokenizar(texto):
    #tokenizo por frases
    #cargamos la libreria en español
    tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
    frases = tokenizer.tokenize(texto)
    
    
    i = 1
    for frase in frases:
        print("frase " + str(i) + ": " + frase)
        
        print("-------------")
        i += 1
        
    tokenizer =  nltk.TreebankWordTokenizer()
    palabras = tokenizer.tokenize(texto)
    frecuencia(palabras)
    i = 1
    

       
#Contar palabras con NLTK
def frecuencia(palabras):
    
    frecuencias = nltk.FreqDist(palabras)
    print(frecuencias)
    print(frecuencias.N)

    
   
    '''
    for token in doc:
        #token.tex lo tokeniza en palabras
   
        
        '''
main()


