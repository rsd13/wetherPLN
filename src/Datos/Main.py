import os
from src.Datos.Precipitacion import Precipitacion
from src.Datos.Nubes import Nubes
from src.Datos.Viento import Viento
from src.Datos.Temperatura import Temperatura






    
def main():
    
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/../textos/csv/crear/"
   
   
    fecha = "2019-01-08"
    nubes = Nubes(path,fecha)
    precipitacion = Precipitacion(path,fecha)
    temperatura = Temperatura(path,fecha)
   
    viento = Viento(path,fecha)
    
   
    
    
    
    informe =  ""
    indice = 0
    
    result = escribirinfore(nubes.frase,indice,informe)
    informe = result[0]
    indice = result[1]
    
    result = escribirinfore(precipitacion.frase,indice,informe)
    informe = result[0]
    indice = result[1]
    
    result = escribirinfore(temperatura.frase,indice,informe)
    informe = result[0]
    indice = result[1]
    print(temperatura.frase)
    result = escribirinfore(viento.frase,indice,informe)
    informe = result[0]
    indice = result[1]
    
    
    informe +=  "\n\n\n"
    informe +=  temperatura.fraseTablaTemperatura
    
    print(informe)
    
    
    
def escribirinfore(frase,indice,informe):
   
   
   
    for c in frase:
       
        
        if indice >= 57:
            
            if c == " ":
                informe +="\n"
                indice = 0
            else: informe +=c
        else: informe +=c
            
        indice +=1
    
    if frase != "":
        informe += " "
    return informe,indice
    
main()



