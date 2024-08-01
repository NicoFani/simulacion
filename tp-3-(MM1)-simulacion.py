import math
import random
import pandas as pd
import matplotlib.pyplot as plt


limite_cola = int(input("Ingrese capacidad máxima de la cola: "))

tiempo_llegada =  [0.0] * (limite_cola +1)
tiempo_prox_evento = [0.0] * 3

cont_cant_cola = [0] * (limite_cola +1) 

def inicializar():
    global tiempo_simulacion, estado_servidor, nro_en_cola, size_queue,tiempo_ultimo_evento, cont_cant_cola, nro_cli_sistema, area_num_en_sistema, area_estado_servidor,area_en_cola,tiempo_total_en_sistema, delay_total, cant_rechazados, cant_cli_atendidos
    
    # Inicializa el reloj de simulacion
    tiempo_simulacion = 0

    # Incializa las variables de estado
    
    # Inicializa contadores estadisticos
    

    # TRUE = Ocupado | FALSE = Libre
    estado_servidor = False
    nro_en_cola = 0
    tiempo_ultimo_evento = 0.0

    # Inicializa lista de eventos, marcando la llegada del primer cliente
    tiempo_prox_evento[1] = tiempo_simulacion + expon(tasa_arribo)
    tiempo_prox_evento[2] = 1.0e+30
    
    # Inicializa los contadores estadisticos
    cant_cli_atendidos = 0
    delay_total = 0.0
    area_en_cola = 0.0
    area_estado_servidor = 0.0

    cont_cant_cola = [0] * (limite_cola +1)
    nro_cli_sistema = 0
    area_num_en_sistema = 0.0
    tiempo_total_en_sistema = 0.0
    cant_rechazados = 0
    global size_queue
    size_queue= pd.DataFrame({'time':[], 'size':[]}) 
    
#TIPO DE EVENTO --> 1:Llegada | 2:Salida


def tiempo():
    global prox_tipo_evento, tiempo_simulacion, tiempo_prox_evento

    prox_tipo_evento = 0
    tiempo_minimo_prox_evento = 1.0e+29
    
    # Se determina el proximo tipo de evento que va a ocurrir
    
    for i in range (1, 3):
        if(tiempo_prox_evento[i] < tiempo_minimo_prox_evento):
            tiempo_minimo_prox_evento = tiempo_prox_evento[i]
            prox_tipo_evento = i
    
    # Se comprueba si la lista de eventos esta vacia, de ser asi, se finaliza la simulacion
    
    if(prox_tipo_evento == 0):
        print("\nLista de evento vacia en tiempo: ", tiempo_simulacion)
        exit(1)

    # Si no esta vacia, se avanza el reloj de simulacion al tiempo del proximo evento
    
    tiempo_simulacion = tiempo_minimo_prox_evento


def llegada():
    global tiempo_prox_evento, tiempo_simulacion, tasa_arribo, nro_cli_sistema, estado_servidor, nro_en_cola, cantidad_clientes, cant_rechazados, tiempo_llegada, cant_cli_atendidos

    tiempo_prox_evento[1] = tiempo_simulacion + expon(tasa_arribo)
    nro_cli_sistema += 1

    # Se comprueba si el servidor esta ocupado
        
    if(estado_servidor == True):
        print("ESTADO SERVER: OCUPADO")
        # Servidor ocupado: se incrementa el numero de clientes en la cola
        nro_en_cola +=1
        # Comprueba si la cola esta llena. Si lo esta, se rechaza el cliente
        print("Se agrega a la cola")
        if(nro_en_cola > limite_cola):
            nro_en_cola -= 1
            cant_rechazados += 1
            print("Cliente rechazado por cola saturada")

        tiempo_llegada[nro_en_cola] = tiempo_simulacion


    else:
        print("ESTADO SERVER: LIBRE")
        # Servidor desocupado: se comienza a servir al cliente y se programa la salida
        estado_servidor = True
        cant_cli_atendidos +=1
        print("Pasa a ser atendido directamente")
        tiempo_prox_evento[2] = tiempo_simulacion + expon(tasa_servicio)
    print("Nro clientes en cola: ", nro_en_cola)

def salida():
    global estado_servidor, nro_en_cola, delay_total, cant_cli_atendidos, tiempo_prox_evento
    global nro_cli_sistema, tiempo_total_en_sistema
    
    # Comprueba que la cola esta vacia
    if(nro_en_cola == 0):
        # La cola está vacía: el servidor está inactivo y se elimina el evento de fin de servicio
        estado_servidor = False
        tiempo_prox_evento[2] = 1.0e+30
    else:
        # La cola no está vacía: se disminuye el número de clientes en la cola}
        print("Cliente nro_en_cola: ", nro_en_cola, " se retira")
        nro_en_cola -=1

        if(nro_cli_sistema > 0):    
            # Disminuye el número de clientes en el sistema
            nro_cli_sistema -=1
        
        # Se calcula la demora del cliente que está iniciando el servicio y se actualiza el acumulador de demora total
        delay = tiempo_simulacion - tiempo_llegada[1]
        delay_total += delay
        
        # Aumenta el tiempo total de clientes en el sistema
        tiempo_total_en_sistema += delay

        # Incrementa el número de clientes retrasados y se programa la salida
        cant_cli_atendidos += 1
        print("Nro de clientes atendidos: ", cant_cli_atendidos)
        tiempo_prox_evento[2] = tiempo_simulacion + expon(tasa_servicio)

        #Se actualiza la cola moviendolos de lugar
        for i in range(1, nro_en_cola + 1):
            tiempo_llegada[i] = tiempo_llegada[i+1]

def reporte():

    # Calcula y devuelve estimaciones de medidas deseadas de rendimiento.
    print("\033[4m" + "Performance measures" + "\033[0m")
    print("Average delay in queue:", round(delay_total / cant_cli_atendidos, 3), "minutes")
    print("Average number in queue:", round(area_en_cola / tiempo_simulacion, 3))
    print("Server utilization:", round(area_estado_servidor / tiempo_simulacion, 3))
    print("Time simulation ended:", round(tiempo_simulacion, 3), "minutes")

    # Nuevas variables
    print("\nAverage number of customers in the system:", round((area_en_cola + area_estado_servidor) / tiempo_simulacion, 3))
    print("Average time in the system:", round(tiempo_total_en_sistema / cant_cli_atendidos, 3), "minutes")
    print("\nProbability of finding n customers in the queue:")
    for n in range(limite_cola + 1):
        probability = cont_cant_cola[n] / tiempo_simulacion
        if (round(probability, 3) != 0.0):
            print(f"* n = {n}: {round(probability*100, 2)}%")

    # Imprime la probabilidad de denegación de servicio}
    print("\nRejected customers:", cant_rechazados)
    print("Rejection probability:", round(cant_rechazados * 100 / cantidad_clientes, 2), "%")
    print(cont_cant_cola)

def update_time_avg_stats():
    global  area_en_cola, area_estado_servidor, nro_en_cola, estado_servidor, tiempo_simulacion, tiempo_ultimo_evento
    global area_num_en_sistema

    # Calcula el tiempo desde el último evento y actualiza el tiempo del último evento
    time_since_last_event = tiempo_simulacion - tiempo_ultimo_evento
    tiempo_ultimo_evento = tiempo_simulacion
    
    # Actualiza el área bajo la función del número en cola
    area_en_cola += nro_en_cola * time_since_last_event
    
    global size_queue
    size_queue=pd.concat([size_queue, pd.DataFrame({'time':tiempo_simulacion, 'size':nro_en_cola}, index=[0])], ignore_index=True)

    # Actualiza el área bajo la función de indicador de servidor ocupado
    area_estado_servidor += estado_servidor * time_since_last_event
    
    # Actualiza el área bajo la función de números de clientes en el sistema y
    # actualiza el número de clientes en cola
    cont_cant_cola[nro_en_cola] += time_since_last_event
    area_num_en_sistema += nro_cli_sistema * time_since_last_event


def expon(tasa):
    return -tasa * math.log(random.random())

def main():

    global cantidad_clientes, tasa_arribo, tasa_servicio
    inicializar()
    while cant_cli_atendidos < cantidad_clientes:
        print("------------------------")
        print("Comienza nuevo evento")
        tiempo()
        print("Se actualiza el reloj tiempo")
        #actualizar contadores estadisticos
        update_time_avg_stats()
        if(prox_tipo_evento == 1):
            print("evento: LLEGADA")
            llegada()
        elif(prox_tipo_evento == 2):
            print("evento: SALIDA")
            salida()
        print("------------------------")

#INICIO_________________________________

tasa_arribo = float(input("Ingrese el tiempo promedio entre arribos: "))
tasa_servicio = float(input("Ingrese el tiempo promedio de servicio: "))
cantidad_clientes = int(input("Ingrese la cantidad de clientes: "))


sum_Average_delay_in_queue = 0
sum_Average_number_in_queue = 0
sum_Server_utilization = 0
sum_Average_number_of_customers_in_the_system = 0
sum_Average_time_in_the_system = 0
sum_Rejection_probabilty = 0
for i in range(3):
    print("************************")
    print('Corrida ',i+1)
    main()
    print("************************")
    sum_Average_delay_in_queue += round(delay_total / cant_cli_atendidos, 3)
    sum_Average_number_in_queue += round(area_en_cola / tiempo_simulacion, 3)
    sum_Server_utilization += round(area_estado_servidor / tiempo_simulacion, 3)
    sum_Average_number_of_customers_in_the_system += round((area_en_cola+ area_estado_servidor) / tiempo_simulacion, 3)
    sum_Average_time_in_the_system += round(tiempo_total_en_sistema / cant_cli_atendidos, 3)
    sum_Rejection_probabilty += round(cant_rechazados * 100 / cantidad_clientes, 2)

print('Cantidad promedio en sistema: ', sum_Average_number_of_customers_in_the_system/10)
print('Cantidad promedio en cola: ', sum_Average_number_in_queue/10)
# print('Tiempo promedio en sistema: ',sum_Average_time_in_the_system/10)
print('Espera promedio en cola: ',sum_Average_delay_in_queue/10)
print('Utilizacion del servidor: ', sum_Server_utilization/10)
print('Probabilidad de rechazo por cola llena: ',sum_Rejection_probabilty/10)

sum_prob_of_n_in_queue=[]
for n in range(limite_cola +1):
    probability = cont_cant_cola[n] / tiempo_simulacion
    if (round(probability, 3) != 0.0):
        print(f"* n = {n}: {round(probability*100, 2)}%")

if input('Mostrar graficas??[s/n]') == 's':
    size_queue.plot(x='time', y='size', kind='line', title="tamaño de la cola en el tiempo")
    fig, ax = plt.subplots()
    arr_sum = sum(cont_cant_cola)
    frecuency_queue_size = [item / arr_sum for item in cont_cant_cola]
    ax.bar(range(len(frecuency_queue_size)), frecuency_queue_size, align='center', alpha=0.7)
    ax.set_xlabel('tamaño de cola')
    ax.set_ylabel('probabliidad')
    ax.set_title('Distribucion de probabilidades del tamaño de la cola')
    plt.show()

