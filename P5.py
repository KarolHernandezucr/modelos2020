#!/usr/bin/env python
# coding: utf-8

# In[7]:


#-----------------Parte 4.1- La encuesta-------------------------------------------------------------


# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from numpy import random
from scipy import stats

def energia_diaria(archivo_json):

    # Cargar el "DataFrame"
    df = pd.read_json(archivo_json) 

    # Convertir en un array de NumPy
    datos = np.array(df)  

    # Crear vector con todos los valores horarios de demanda
    demanda = []

    # Extraer la magnitud de la demanda para todas las horas
    for hora in range(len(datos)):
        demanda.append(datos[hora][0]['MW'])

    # Separar las magnitudes en grupos de 24 (24 h)
    demanda = np.split(np.array(demanda), len(demanda) / 24)

    # Crear vector para almacenar la energía a partir de la demanda
    energia = []
    
    # Calcular la energía diaria por la regla del trapecio
    for dia in range(len(demanda)):
        E = round(np.trapz(demanda[dia]), 2)
        energia.append(E)

    return energia

def definicion_estados(vector_energia, estados):

    minimo = np.min(vector_energia)
    maximo = np.max(vector_energia) + 1
    segmento = (maximo - minimo)/estados
    vector_estados = np.empty(len(vector_energia))
    
    for i, dia in enumerate(vector_energia):
        diferencia = dia - minimo
        proporcion = diferencia // segmento
        vector_estados[i] = proporcion + 1
        
    return vector_estados

def probabilidad_transicion(vector_estados, numero_estados, presente, futuro):
   
    # Recorrer el vector_estados
    ocurrencias_i = 0
    ocurrencias_i_j = 0
    for i, estado in enumerate(vector_estados[0:-1]):
        if estado == presente:
            ocurrencias_i += 1
            if vector_estados[i+1] == futuro:
                ocurrencias_i_j += 1
    
    # Cálculo de la probabilidad
    probabilidad = ocurrencias_i_j / ocurrencias_i
    
    return probabilidad

def parametros_asignados(digitos):
    '''Elige un valor t aleatoriamente,
    dos estados arbitrarios i y j
    '''
    
    random.seed(digitos)
    estados = [i+1 for i in range(10)]
    T = stats.expon(2)
    t = int(T.rvs())
    i = estados[random.randint(0, len(estados))]
    j = estados[random.randint(0, len(estados))]
    print('t: {}, i: {}, j: {}'.format(t, i, j))
    return t, i, j

# Importamos los datos para calular la energía diaria
vector_energia = energia_diaria('demanda_2019.json')

# Definir los estados a trabajar 
numero_estados = 10
vector_estados = definicion_estados(vector_energia, numero_estados)
# Imprimo los estados en forma de vector
print(vector_estados)

# Definir la probabilidad de transición de "i" a "j"
i, j = 10, 9
Pi_ij = probabilidad_transicion(vector_estados, numero_estados, i, j)
print('Pi_ij =', Pi_ij)

#------------------ Parte 4.2 del proyecto--------------------------------------------------------------------


print("---------Asignación 4.2----------")

numero_estados = 10
Px_xy = np.zeros((10,10))

# Conforme el siguiente for 
for conta in range(1, numero_estados+1):
    
    for conta2 in range(1, numero_estados+1):
        
            Px_xy[conta-1][conta2-1] = probabilidad_transicion(vector_estados, numero_estados, conta, conta2)


print("Matriz de transición de estados es la siguiente: \n")    

print(Px_xy, "\n")   

#-------------------------- Parte 4.3 del proyecto------------------------------------------

print("--------- Asignación 4.3---------")

#Asignación de parámetros de acuerdo al carne B63367


print("Parámetros asignados:")
t, i, j = parametros_asignados(63367)

# Matriz de orden t

Px_xyo = Px_xy 
conta = 0

for conta in range(1, t):

    Px_xyo = np.dot(Px_xyo,Px_xy)


# Se imprimen los resultados obtenidos

print("Matriz de transición de orden:", t, " \n")
print(Px_xyo)

print("La probabilidad de estar en el estado ", j, ", ", t," días después de estar en el estado ", i, " es de: ", Px_xyo[i-1][j-1])    


# In[ ]:





# In[ ]:




