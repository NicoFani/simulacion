import random
import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 7 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-e":
    print("Uso: tp1-simulacion.py -c <rango> -n <corridas> -e <nro>")
    sys.exit(1)

rango = int(sys.argv[2])
corridas = int(sys.argv[4])
nro = int(sys.argv[6])

## Diccionarios para guardar los valores de cada corrida
lista_frec_relativa_corridas = {}
lista_promedio_corridas = {}
lista_desvio_corridas = {}
lista_varianza_corridas = {}

for i in range(corridas):

    ## SIMULACION de Valores
    valores = [random.randint(0, 36) for _ in range(rango)]

    ## CALCULO de Frecuencia Relativa para histograma
    frec_relativa_por_nro = {}
    for j in range(37):
        frec_relativa_por_nro[j] = valores.count(j) / rango


    ## CALCULO de Frecuencia Relativa, Promedio, Desvio y Varianza
    lista_frec_relativa_nro = []
    for j in range(1, rango+1):
        lista_frec_relativa_nro.append(valores[:j].count(nro)/j)
    lista_frec_relativa_corridas[i] = lista_frec_relativa_nro
    lista_esperada_relativa = [1/37 for j in range(rango)]

    lista_promedio = []
    for j in range(1, rango+1):
        lista_promedio.append(sum(valores[:j])/j)
    lista_promedio_corridas[i] = lista_promedio
    lista_esperada_promedio = [1/37*666 for j in range(rango)]

    lista_desvio = []
    for j in range(1, rango+1):
        lista_desvio.append(np.std(valores[:j]))
    lista_desvio_corridas[i] = lista_desvio
    lista_esperada_desvio = [37/np.sqrt(12) for j in range(rango)]

    lista_varianza = []
    for j in range(1, rango+1):
        lista_varianza.append(np.var(valores[:j]))
    lista_varianza_corridas[i] = lista_varianza
    lista_esperada_varianza = [37**2/12 for j in range(rango)]


    ## GRAFICAS 
    plt.figure(figsize=(12, 10))

    plt.subplot(2, 2, 1)
    plt.plot(lista_frec_relativa_nro, label='Frecuencia Relativa de Nro', color='blue')
    plt.xlabel('Número de tirada')
    plt.ylabel('Frec. relativa obtenida')
    plt.plot(lista_esperada_relativa, label='Frecuencia Relativa Esperada', color='red')
    plt.title("Frecuencia Relativa vs. Frecuencia esperada")
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(lista_promedio, label='Promedio', color='blue')
    plt.xlabel('Número de tirada')
    plt.ylabel('Promedio Obtenido')
    plt.plot(lista_esperada_promedio, label='Promedio Esperado', color='red')
    plt.title("Promedio vs. Promedio esperado")
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(lista_desvio, label='Desvio', color='blue')
    plt.xlabel('Número de tirada')
    plt.ylabel('Desvio Obtenido')
    plt.plot(lista_esperada_desvio, label='Desvio Esperado', color='red')
    plt.title("Desvio vs. Desvio esperado")
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(lista_varianza, label='Varianza', color='blue')
    plt.xlabel('Número de tirada')
    plt.ylabel('Varianza Obtenida')
    plt.plot(lista_esperada_varianza, label='Varianza Esperada', color='red')
    plt.title("Varianza vs. Varianza esperada")
    plt.legend()

    plt.savefig('Corrida%s.png'% (i))

    plt.figure(figsize=(15, 6))
    plt.bar(frec_relativa_por_nro.keys(), frec_relativa_por_nro.values())
    plt.axhline(1/37, color='red', linestyle='--', linewidth=2, label='Frec. Relativa Esperado')
    plt.xlabel('Resultado')
    plt.ylabel('Frecuencia Relativa')
    plt.title('Histograma Frecuencia Relativa de los valores por Corrida')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('Histograma%s.png'% (i))

## GRAFICAS DE TODAS LAS CORRIDAS

plt.figure(figsize=(15, 6))
for i in range(corridas):    
    plt.plot(range(1, rango+1), lista_frec_relativa_corridas[i], label=f'Corrida {i+1}')
plt.axhline(1/37, color='red', linestyle='--', linewidth=2, label='Frec. Relativa Esperado')
plt.xlabel('Número de tiradas')
plt.ylabel('Frec. relativa obtenida')
plt.title("Frecuencia Relativa vs. Frecuencia esperada")
plt.legend()
plt.savefig('FrecuenciaRelativa.png')

plt.figure(figsize=(15, 6))
for i in range(corridas):    
    plt.plot(range(1, rango+1), lista_promedio_corridas[i], label=f'Corrida {i+1}')
plt.axhline(1/37*666, color='red', linestyle='--', linewidth=2, label='Promedio Esperado')
plt.xlabel('Número de tiradas')
plt.ylabel('Promedio obtenido')
plt.title("Promedio obtenido vs. Promedio esperado")
plt.legend()
plt.savefig('Promedio.png')

plt.figure(figsize=(15, 6))
for i in range(corridas):    
    plt.plot(range(1, rango+1), lista_desvio_corridas[i], label=f'Corrida {i+1}')
plt.axhline(37/np.sqrt(12), color='red', linestyle='--', linewidth=2, label='Desvio Esperado')
plt.xlabel('Número de tiradas')
plt.ylabel('Desvio obtenido')
plt.title("Desvio obtenido vs. Desvio esperado")
plt.legend()
plt.savefig("Desvio.png")

plt.figure(figsize=(15, 6))
for i in range(corridas):    
    plt.plot(range(1, rango+1), lista_varianza_corridas[i], label=f'Corrida {i+1}')
plt.axhline(37**2/12, color='red', linestyle='--', linewidth=2, label='Frec. Relativa Esperado')
plt.xlabel('Número de tiradas')
plt.ylabel('Varianza obtenida')
plt.title("Varianza obtenida vs. Varianza esperada")
plt.legend()
plt.savefig('Varianza.png')
##plt.show()
