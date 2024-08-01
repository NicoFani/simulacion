import math
import random
import matplotlib.pyplot as plt

cantidad = 0
grandes = 0
nivel_inv_inicial = 0
nivel_inv = 0
tipo_prox_evento = 0
num_eventos = 0
num_meses = 0
num_valores_demanda = 0
pequeños = 0
area_almacenamiento = 0.0
area_desabastecimiento = 0.0
costo_almacenamiento = 0.0
costo_incremental = 0.0
max_retraso = 0.0
media_interdemanda = 0.0
min_retraso = 0.0
distribucion_prob_demanda = []
costo_configuracion = 0.0
costo_desabastecimiento = 0.0
tiempo_simulacion = 0.0
tiempo_ultimo_evento = 0.0
tiempo_prox_evento = [0.0] * 5
costo_total_pedidos = 0.0
total_final = 0.0
almacenamiento_final = 0.0
desabastecimiento_final = 0.0
pedido_final = 0.0
costos_totales = []
costos_pedidos = []
costos_almacenamiento = []
costos_desabastecimiento = []
total_por_politica = []
pedido_por_politica = []
almacenamiento_por_politica = []
desabastecimiento_por_politica = []

def inicializar():
    global tiempo_simulacion, nivel_inv, tiempo_ultimo_evento, costo_total_pedidos, area_almacenamiento, area_desabastecimiento, tiempo_prox_evento
    global total_final, almacenamiento_final, desabastecimiento_final, pedido_final

    # Inicializa el reloj de simulación
    tiempo_simulacion = 0.0

    # Inicializa las variables de estado
    nivel_inv = nivel_inv_inicial
    tiempo_ultimo_evento = 0.0

    # Inicializa los contadores estadísticos
    costo_total_pedidos = 0.0
    area_almacenamiento = 0.0
    area_desabastecimiento = 0.0

    # Inicializa la lista de eventos. Como no hay pedidos pendientes, el evento de llegada 
    # del pedido se elimina de la consideración
    tiempo_prox_evento[1] = 1.0e+30
    tiempo_prox_evento[2] = tiempo_simulacion + expon(media_interdemanda)
    tiempo_prox_evento[3] = num_meses
    tiempo_prox_evento[4] = 0.0

def llegada_pedido():
    global nivel_inv, tiempo_prox_evento

    # Aumenta el nivel del inventario por la cantidad ordenada
    nivel_inv += cantidad

    # Como no hay pedidos pendientes, elimina el evento de llegada del pedido de la consideración
    tiempo_prox_evento[1] = 1.0e+30

def demanda():
    global nivel_inv, tiempo_prox_evento

    # Reduce el nivel del inventario por el tamaño de una demanda generada
    nivel_inv -= entero_aleatorio(distribucion_prob_demanda)

    # Programa la hora de la siguiente demanda
    tiempo_prox_evento[2] = tiempo_simulacion + expon(media_interdemanda)

def evaluar():
    global nivel_inv, cantidad, costo_total_pedidos, tiempo_prox_evento

    # Comprueba si el nivel del inventario es menor que "pequeños"
    if nivel_inv < pequeños:

        # Como el nivel del inventario es menor a "pequeños", se hace un pedido por la cantidad adecuada
        cantidad = grandes - nivel_inv
        costo_total_pedidos += costo_configuracion + costo_incremental * cantidad

        # Programa la llegada del pedido
        tiempo_prox_evento[1] = tiempo_simulacion + uniforme(min_retraso, max_retraso)

    # Sin importar la decisión de realizar el pedido, se programa la próxima evaluación de inventario
    tiempo_prox_evento[4] = tiempo_simulacion + 1.0

def reporte():
    global area_almacenamiento, area_desabastecimiento, costo_total_pedidos, num_meses, pequeños, grandes, costo_almacenamiento, costo_desabastecimiento
    global total_final, almacenamiento_final, desabastecimiento_final, pedido_final
    global costos_totales, costos_pedidos, costos_almacenamiento, costos_desabastecimiento
    global total_por_politica, pedido_por_politica, almacenamiento_por_politica, desabastecimiento_por_politica

    # Calcula y devuelve estimaciones de medidas deseadas de rendimiento.
    costo_prom_almacenamiento = costo_almacenamiento * area_almacenamiento / num_meses
    costo_prom_desabastecimiento = costo_desabastecimiento * area_desabastecimiento / num_meses
    costo_prom_pedidos = costo_total_pedidos / num_meses

    # Suma el acumulado total
    total_final += costo_prom_almacenamiento + costo_prom_desabastecimiento + costo_prom_pedidos
    almacenamiento_final += costo_prom_almacenamiento
    desabastecimiento_final += costo_prom_desabastecimiento
    pedido_final += costo_prom_pedidos

    total_por_politica.append(costo_prom_almacenamiento + costo_prom_desabastecimiento + costo_prom_pedidos)
    pedido_por_politica.append(costo_prom_pedidos)
    almacenamiento_por_politica.append(costo_prom_almacenamiento)
    desabastecimiento_por_politica.append(costo_prom_desabastecimiento)

    costos_totales.append(costo_prom_almacenamiento + costo_prom_desabastecimiento + costo_prom_pedidos)
    costos_pedidos.append(costo_prom_pedidos)
    costos_almacenamiento.append(costo_prom_almacenamiento)
    costos_desabastecimiento.append(costo_prom_desabastecimiento)

    print("\n\n({}, {}){:>15.2f}{:>15.2f}{:>15.2f}{:>15.2f}".format(
        pequeños, grandes, costo_prom_pedidos + costo_prom_almacenamiento + costo_prom_desabastecimiento,
        costo_prom_pedidos, costo_prom_almacenamiento, costo_prom_desabastecimiento))

def actualizar_estad_prom_tiempo():
    global tiempo_simulacion, tiempo_ultimo_evento, nivel_inv, area_desabastecimiento, area_almacenamiento

    # Calcula el tiempo desde el último evento y actualiza el tiempo del último evento
    tiempo_desde_ultimo_evento = tiempo_simulacion - tiempo_ultimo_evento
    tiempo_ultimo_evento = tiempo_simulacion

    # Determina el estado del nivel del inventario durante el intervalo anterior
    # Si el nivel del inventario durante el intervalo anterior era negativo, se actualiza area_desabastecimiento
    # Si era positivo, se actualiza area_almacenamiento
    # Si era cero no se actualiza nada
    if nivel_inv < 0:
        area_desabastecimiento -= nivel_inv * tiempo_desde_ultimo_evento
    elif nivel_inv > 0:
        area_almacenamiento += nivel_inv * tiempo_desde_ultimo_evento

def expon(media):
    # Devuelve una variable aleatoria exponencial con media "media"
    return -media * math.log(random.random())

def entero_aleatorio(distribucion_prob):
    u = random.random()
    # Retorna un entero aleatorio de acuerdo con la función de distribución acumulativa "distribucion_prob"
    i = 1
    while u >= distribucion_prob[i]:
        i += 1
    return i

def uniforme(a, b):
    # Función de generación de una variable uniforme. Devuelve una variable aleatoria U(a, b)
    return a + random.random() * (b - a)

def temporizacion():
    global tiempo_simulacion, tipo_prox_evento, tiempo_prox_evento, num_eventos

    # Determina el siguiente tipo de evento y avanza el reloj de simulación
    min_tiempo_prox_evento = 1.0e+30
    tipo_prox_evento = 0

    for i in range(1, num_eventos + 1):
        if tiempo_prox_evento[i] < min_tiempo_prox_evento:
            min_tiempo_prox_evento = tiempo_prox_evento[i]
            tipo_prox_evento = i

    if tipo_prox_evento == 0:
        print("Lista de eventos vacía en el tiempo {}".format(tiempo_simulacion))
        exit(1)

    tiempo_simulacion = min_tiempo_prox_evento

def graficas_costos(costos_totales, costos_pedidos, costos_almacenamiento, costos_desabastecimiento, pequeñosArray, grandesArray):
    
    politicas = []

    for pequeño, grande in zip(pequeñosArray, grandesArray):
        politica = f"{pequeño}-{grande}"
        politicas.append(politica)


    # Configuración de la gráfica de barras
    x = range(len(politicas))
    ancho = 0.2

    fig, ax = plt.subplots(figsize=(10, 8))

    # Crear las barras
    ax.bar(x, costos_totales, width=ancho, label='Costo Total')
    ax.bar([i + ancho for i in x], costos_pedidos, width=ancho, label='Costo de Pedidos')
    ax.bar([i + 2 * ancho for i in x], costos_almacenamiento, width=ancho, label='Costo de Almacenamiento')
    ax.bar([i + 3 * ancho for i in x], costos_desabastecimiento, width=ancho, label='Costo de Desabastecimiento')

    # Configuración de etiquetas y títulos
    ax.set_xlabel('Políticas')
    ax.set_ylabel('Costos')
    ax.set_title('Comparación de Costos por Política')
    ax.set_xticks([i + 1.5 * ancho for i in x])
    ax.set_xticklabels(politicas)
    ax.legend()

    plt.show()


def grafico_costos_por_tiempo(num_meses, costos_totales, costos_pedidos, costos_almacenamiento, costos_desabastecimiento):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_meses + 1), costos_totales, marker='o', linestyle='-', label='Costos Totales')
    plt.plot(range(1, num_meses + 1), costos_pedidos, marker='s', linestyle='--', label='Costos de Pedidos')
    plt.plot(range(1, num_meses + 1), costos_almacenamiento, marker='^', linestyle='--', label='Costos de Almacenamiento')
    plt.plot(range(1, num_meses + 1), costos_desabastecimiento, marker='d', linestyle='--', label='Costos de Desabastecimiento')

    plt.xlabel('Meses')
    plt.ylabel('Valor')
    plt.title('Variación de costos a lo largo del tiempo')
    plt.legend()

    # Mostrar la gráfica
    plt.show()

def main():
    global cantidad, grandes, nivel_inv_inicial, nivel_inv, tipo_prox_evento, num_eventos, num_meses, num_valores_demanda, pequeños, area_almacenamiento, area_desabastecimiento, costo_almacenamiento, costo_incremental, max_retraso, media_interdemanda, min_retraso, distribucion_prob_demanda, costo_configuracion, costo_desabastecimiento, tiempo_simulacion, tiempo_ultimo_evento, tiempo_prox_evento, costo_total_pedidos, total_final, almacenamiento_final, desabastecimiento_final, pedido_final, costos_totales, costos_pedidos, costos_almacenamiento, costos_desabastecimiento, total_por_politica, pedido_por_politica, almacenamiento_por_politica, desabastecimiento_por_politica, num_politicas

    num_eventos = 4
    k = 0

    # Inicialización de parámetros
    nivel_inv_inicial = 60
    num_meses = 9
    num_politicas = 9
    num_valores_demanda = 4
    media_interdemanda = 0.10
    costo_configuracion = 32
    costo_incremental = 3
    costo_almacenamiento = 1
    costo_desabastecimiento = 5
    min_retraso = 0.5
    max_retraso = 1.0


# costo_configuracion = float(input("Ingrese el costo configuracion: "))
# costo_incremental = float(input("Ingrese el costo incremental: "))
# costo_almacenamiento = float(input("Ingrese el costo almacenamiento: "))
# costo_desabastecimiento = float(input("Ingrese el costo desabastecimiento: "))


    # Distribución de probabilidad de la demanda
    distribucion_prob_demanda = [0.0] * (int(num_valores_demanda) + 1)
    for i in range(1, int(num_valores_demanda) + 1):
        distribucion_prob_demanda[i] = float(input("Ingrese el valor de prob_distrib_demand en {}: ".format(i)))



    # Imprime los parámetros de entrada
    print("\n\n\n\n" + "\033[4m" + "Single-product inventory system" + "\033[0m")
    print("\nInitial inventory level{:>24} items".format(int(nivel_inv_inicial)))
    print("Number of demand sizes{:>25}".format(int(num_valores_demanda)))
    print("Distribution function of demand sizes \t  ", end=" ")
    numbers = []
    for i in range(1, int(num_valores_demanda) + 1):
        numbers.append(str(distribucion_prob_demanda[i]))
    print("   ".join(numbers))
    print("Mean interdemand time{:>26.2f} months".format(media_interdemanda))
    print("Delivery lag range{:>29.2f} to {:.2f} months".format(min_retraso, max_retraso))
    print("Length of the simulation{:>23} months".format(int(num_meses)))
    print("K = {:.1f}    i = {:.1f}    h = {:.1f}    pi = {:.1f}".format(costo_configuracion, costo_incremental, costo_almacenamiento, costo_desabastecimiento))
    print("Number of policies{:>29}\n".format(int(num_politicas)))
    print("              Average         Average         Average              Average")
    print("Politica     Costo Total    Costo Pedido  Costo Mantenimiento   Costo Faltante")

    # Definición de políticas de revisión (s, S)
    politicas = [(20, 40), (20, 60), (20, 80), (20, 100), (40,60), (40, 80), (40, 100), (60, 80), (60, 100)]

    # Ejecución de la simulación para cada política
    for s, S in politicas:
        pequeños = s
        grandes = S
        inicializar()
        while True:
            temporizacion()
            actualizar_estad_prom_tiempo()
            if tipo_prox_evento == 1:
                llegada_pedido()
            elif tipo_prox_evento == 2:
                demanda()
            elif tipo_prox_evento == 3:
                reporte()
            elif tipo_prox_evento == 4:
                evaluar()
            
            if tipo_prox_evento == 3:
                break
        k += 1

    print("\n\n" + "\033[4m" + "Costos Finales" + "\033[0m")
    print("Costo Total:", round(total_final, 2))
    print("Costo de Orden:", round(pedido_final, 2))
    print("Costo de Mantenimiento:", round(almacenamiento_final, 2))
    print("Costo de Faltante:", round(desabastecimiento_final, 2))

    # Gráficas de los costos por política
    graficas_costos(costos_totales, costos_pedidos, costos_almacenamiento, costos_desabastecimiento, [p[0] for p in politicas], [p[1] for p in politicas])
    grafico_costos_por_tiempo(num_meses, costos_totales, costos_pedidos, costos_almacenamiento, costos_desabastecimiento)

main()