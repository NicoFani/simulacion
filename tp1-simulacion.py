import random
import sys
import numpy as np

if len(sys.argv) !=3  or sys.argv[1] != "-n":
    
    print("Uso: tp1-simulacion.py -n <rango>")
    sys.exit(1)

rango = int(sys.argv[2])

valores = [random.randint(0, 36) for _ in range(rango)]

print(valores)

frec_absoluta = {}
frec_relativa = {}
promedio = {}
count = 0

# for i in range (37):
#     frec_absoluta[i] = valores.count(i)

# for i in range (37):
#     frec_relativa[i] = frec_absoluta[i]/rango

prom = sum(valores)/len(valores)
desvio = np.std(valores)

print()
print("Frecuencia absoluta", frec_absoluta)
print()
print("Frecuencia relativa", frec_relativa)
print()
print("Promedio:", prom)
print()
print("Desvio estandar", desvio)
