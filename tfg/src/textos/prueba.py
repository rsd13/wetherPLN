'''
Created on Feb 4, 2019

@author: rafaelsoriadiez
'''




import math

lista = [0,1]


i = 0
suma = 0
while (i < 100):
    suma = 0
    suma = lista[i] + lista[i + 1]
    lista.append(suma)
    print(lista[i])
    i = i + 1
    
i = 0
suma = 0
while (i < len(lista)):
    suma += lista[i]
    i += 1

media = suma/len(lista)
print("----")
print(media)

i = 0
suma = 0
aux = 0
while( i < len(lista)):
    aux = lista[i] - media
    aux = aux * aux
    
    suma += aux
    

    i += 1

print(math.sqrt(suma))
