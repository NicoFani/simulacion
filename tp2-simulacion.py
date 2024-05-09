import random
import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 11 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-e" or sys.argv[7] != "-s" or sys.argv[9] != "-a":
    print("Uso: tp1-simulacion.py -c <rango> -n <corridas> -e <color> -s <estrategia> -a <tipo_capital>")
    sys.exit(1)

nro_rojo = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
nro_negro = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]


tiradas = int(sys.argv[2])
corridas = int(sys.argv[4])
## r (rojo), n (negro)
color = sys.argv[6]
## m (martingala), d (D’Alambert), f (Fibonacci), o (otra)
estrategia = sys.argv[8]
## i (infinito), f (finito)
tipo_capital = sys.argv[10]

apuesta_inicial = 5

def tirar_ruleta(apuesta:float, color:str):
    resultado = random.randint(0, 36)
    if((color == 'r' and resultado in nro_rojo) or (color == 'n' and resultado in nro_negro)):
        return apuesta*2
    else:
        return 0


for i in range(corridas):
    if(tipo_capital == 'f'):
        capital = 100
    else:
        capital = 0
    fib_anterior = 3
    fib_actual = apuesta_inicial
    apuesta = apuesta_inicial
    historial = []
    if (tipo_capital == 'f'):
        cont_tiradas = 0
        while (cont_tiradas <= tiradas and capital>0):
            resultado = tirar_ruleta(apuesta, color)
            capital -= apuesta
            print("apuesta:", apuesta)
            if(resultado != 0):
                capital += resultado
                if(estrategia == 'm'):
                    apuesta = apuesta_inicial
                elif(estrategia == 'd'):
                    apuesta -= 1

                elif(estrategia == 'f'):
                    print("actual: ",fib_actual)
                    print("anterior: ", fib_anterior)
                    apuesta = fib_actual - fib_anterior
                    if(fib_anterior-fib_actual <= 0):
                        fib_actual = 1
                        apuesta = fib_actual
                        fib_anterior = 0
                    else: 
                        fib_actual = apuesta
                        fib_anterior = fib_anterior - fib_actual 
                print("--gano-- ", resultado)
                print("capital: ", capital)
            else:
                if(estrategia == 'm'):
                    apuesta = apuesta*2
                elif(estrategia == 'd'):
                    apuesta += 1
                    
                elif(estrategia == 'f'):
                    print("actual: ",fib_actual)
                    print("anterior: ", fib_anterior)
                    apuesta = fib_actual + fib_anterior
                    fib_anterior = fib_actual
                    fib_actual = apuesta
                print("---perdio---")
                print("proxima apuesta: ", apuesta)
            cont_tiradas += 1
            historial.append(capital)
        
    else:
        for i in range(tiradas):
            resultado = tirar_ruleta(apuesta, color)
            capital -= apuesta
            if(resultado != 0):
                capital += resultado
                if(estrategia == 'm'):
                    apuesta = apuesta_inicial
                elif(estrategia == 'd'):
                    apuesta -= 1
                elif(estrategia == 'f'):
                    apuesta = fib_actual - fib_anterior
                    if(fib_anterior-fib_actual <= 0):
                        fib_actual = 1
                        fib_anterior = 0
                    else: 
                        fib_actual = apuesta
                        fib_anterior = fib_anterior - fib_actual
            else:
                if(estrategia == 'm'):
                    apuesta = apuesta*2
                elif(estrategia == 'd'):
                    apuesta += 1
                elif(estrategia == 'f'):
                    apuesta = fib_actual + fib_anterior
                    fib_anterior = fib_actual
                    fib_actual = apuesta
        historial.append(capital)
    print(historial)

    # crearGraficas(historial, tiradas)










