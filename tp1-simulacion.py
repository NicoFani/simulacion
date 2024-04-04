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

valores = [random.randint(0, 36) for _ in range(rango)]

print(valores)

frec_relativa = valores.count(nro) / rango
promedio = {}
count = 0

prom = sum(valores)/len(valores)
desvio = np.std(valores)
varianza = np.var(valores)


print()
print("Frecuencia relativa", frec_relativa)
print("Frecuencia relativa esperada", 1/37)
print()
print("Promedio:", prom)
print("Promedio Esperado", 38/2)
print()
print("Desvio estandar", desvio)
print("Desvio estandar esperado", 38/np.sqrt(12))
print()
print("Varianza", varianza)
print("Varianza esperada", 38**2/12)

## GRAFICAS
lista_frec_relativa_nro = []
frec_relativa
# for i in range(valores):
#     frec_relativa = valores_nro.count(nro) / i
#     lista_frec_relativa_nro.append(frec_relativa)
lista1 = [0.1, 0.1, 0.3, 0.3, 0.3, 0.35, 0.35, 0.4, 0.5]
lista2 = [1/37 for i in range(rango)]
print(lista_frec_relativa_nro)
plt.plot(lista1, label='Frecuencia Relativa de Nro', color='blue')
plt.xlabel('Número de tirada')
plt.ylabel('Valor obtenido')
plt.plot(lista2, label='Frecuencia Relativa Esperada', color='red')
plt.title('Frecuencia Relativa de Nro')
plt.savefig('frec-relativa.png')

# DESPUES DEL CORRER EL TOTAL DE CORRIDAS --> Mostrar frecuencia relativa de cada numero
#                                         --> 

# for i in range (37):
#     frec_absoluta[i] = valores.count(i)

# for i in range (37):
#     frec_relativa[i] = frec_absoluta[i]/rango