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
## m (Martingala), d (D’Alambert), f (Fibonacci), o (Paroli (Martingala-inversa))
estrategia = sys.argv[8]
## i (infinito), f (finito)
tipo_capital = sys.argv[10]

apuesta_inicial = 5
cont_bancarrota = {}
list_historial_capital = []


def tirar_ruleta(apuesta:float, color:str):
    resultado = random.randint(0, 36)
    if((color == 'r' and resultado in nro_rojo) or (color == 'n' and resultado in nro_negro)):
        return apuesta*2
    else:
        return 0
    
def CalcularFrecRelativa(historial_resultados, tiradas):
    frec_relativa_por_tirada = {}
    for j in range(1, tiradas + 1):
        ganadas = historial_resultados[:j].count(1)
        frec_relativa_por_tirada[j] = ganadas / j 
    return frec_relativa_por_tirada

def crearGraficasTiradas(historial_capital, tiradas, i):
    # Grafica de Capital por corrida
    plt.figure(figsize=(12, 10))
    plt.subplot(2, 1, 1)
    plt.plot(historial_capital, label='Capital', color='blue')
    plt.xlabel('Tiradas')
    plt.ylabel('Capital')
    if(tipo_capital == 'f'):
        plt.plot( [100 for i in range(tiradas)], label='Tiradas', color='purple')
        plt.plot( [0 for i in range(tiradas)], label='Bancarrota', color='red', linestyle='--')
    else:
        plt.plot( [0 for i in range(tiradas)], label='Cero', color='purple')
    plt.legend()
    plt.title("Capital vs. Capital Inicial")
    plt.savefig('Corrida%s.png'% (i))

    #Grafica Frec.Relativa de obtener apuesta favorable segun n
    frec_relativa = CalcularFrecRelativa(historial_resultados, tiradas)
    plt.figure(figsize=(12, 10))
    plt.subplot(2, 1, 1)
    plt.bar(frec_relativa.keys(), frec_relativa.values(), label='Frec.Relativa favorable', color='blue')
    plt.xlabel('Tiradas')
    plt.ylabel('Frec. Relativa')
    plt.title("Frec.Relativa favorable segun n")
    plt.savefig('Frec.Relativa%s.png'% (i))

def crearGraficasCorrida(cont_bancarrota, corridas):
    plt.figure(figsize=(12, 10))
    plt.bar(cont_bancarrota.keys(), cont_bancarrota.values(), label='bancarrota', color='blue')
    plt.xlabel('Cantidad de corridas')
    plt.ylabel('Bancarrota')
    plt.axhline(contarBancarrotas(cont_bancarrota)/corridas, color='red', linestyle='--', linewidth=2, label='Promedio Bancarrota')
    plt.legend()
    plt.title("Bancarrota por Corrida")
    plt.savefig('ContadorBancarrota%s.png'% (i))


def contarBancarrotas(cont_bancarrota):
    return sum(1 for valor in cont_bancarrota.values() if valor == 1)

for i in range(corridas):
    if(tipo_capital == 'f'):
        capital = 100
    else:
        capital = 0

    list_resultados = [] 

    historial_resultados = []
    fib_anterior = 3
    fib_actual = apuesta_inicial

    apuesta = apuesta_inicial

    historial_capital = []

    if (tipo_capital == 'f'):
        cont_tiradas = 0
        historial_capital.append(capital)
        capital -= apuesta
        while (cont_tiradas <= tiradas and capital>0):
            resultado = tirar_ruleta(apuesta, color)
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
                        apuesta = fib_actual
                        fib_anterior = 0
                    else: 
                        fib_actual = apuesta
                        fib_anterior = fib_anterior - fib_actual 
                elif(estrategia == 'o'):
                        apuesta = apuesta*2
                historial_resultados.append(1)
                        
            else:
                if(estrategia == 'm'):
                    apuesta = apuesta*2
                elif(estrategia == 'd'):
                    apuesta += 1                   
                elif(estrategia == 'f'):
                    apuesta = fib_actual + fib_anterior
                    fib_anterior = fib_actual
                    fib_actual = apuesta
                elif(estrategia == 'o'):
                    apuesta = apuesta_inicial
                historial_resultados.append(0)   
            cont_tiradas += 1
            historial_capital.append(capital)
            if(capital-apuesta <= 0): 
                apuesta = capital
                capital -= apuesta
            else:
                capital -= apuesta
        if(capital-apuesta <= 0): 
            cont_bancarrota[i+1] = 1
            historial_capital.append(0)
        else:
            cont_bancarrota[i+1] = 0
            
             
        
    else:
        for j in range(tiradas):
            capital -= apuesta
            resultado = tirar_ruleta(apuesta, color)
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
                elif(estrategia == 'o'):
                    apuesta = apuesta*2
                historial_resultados.append(1)
            else:
                if(estrategia == 'm'):
                    apuesta = apuesta*2
                elif(estrategia == 'd'):
                    apuesta += 1
                elif(estrategia == 'f'):
                    apuesta = fib_actual + fib_anterior
                    fib_anterior = fib_actual
                    fib_actual = apuesta
                elif(estrategia == 'o'):
                    apuesta = apuesta_inicial
                historial_resultados.append(0)
            historial_capital.append(capital)

    crearGraficasTiradas(historial_capital, tiradas, i)

crearGraficasCorrida(cont_bancarrota, corridas)






    



