import numpy as np
import math
import random
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import chisquare
from scipy.stats import stats
from scipy.stats import uniform

# *****************************************************************
# ************ GENERADORES DE NUMEROS PSEUDOALEATORIOS ************
# *****************************************************************


# ----------------- Metodo de los cuadrados medios -----------------

def seed_generator(number:int)->int:
    if not isinstance(number, int):
        raise ValueError("Input must be an integer.")
    number_str=str(number);
    if(len(number_str)==8):
        return int(number_str[2:-2])
    elif(len(number_str)==7):
        return int(number_str[1:-2])
    elif(len(number_str)<=6 and len(number_str)>=3):
      return int(number_str[0:-2])
    else:
      return 0

def mid_square(initial_seed:int ,num_iterations:int):
  if(len(str(initial_seed)) <4 ):
    raise ValueError("Seed value must have at least 4 digits.");
  values = [0 for _ in range(num_iterations)]
  seeds = [0 for _ in range(num_iterations)]
  values[0] = pow(initial_seed,2)
  seeds[0]= seed_generator(values[0]);
  for i in range(num_iterations-1):
    if(values[i]==0):break;
    values[i+1]=pow(seeds[i],2);
    seeds[i+1]=seed_generator(values[i+1]);  
  return np.divide(values,100_000_000)

def mid_square_no_div(initial_seed:int ,num_iterations:int):
  if(len(str(initial_seed)) <4 ):
    raise ValueError("Seed value must have at least 4 digits.");
  values = [0 for _ in range(num_iterations)]
  seeds = [0 for _ in range(num_iterations)]
  values[0] = pow(initial_seed,2)
  seeds[0]= seed_generator(values[0]);
  for i in range(num_iterations-1):
    if(values[i]==0):break;
    values[i+1]=pow(seeds[i],2);
    seeds[i+1]=seed_generator(values[i+1]);  
  return values

# print(mid_square(1232,1000))



# ----------------- Generador Congruencial Lineal (GCL) -----------------

def generate_number_base(module, multiplicator, increment, initial_seed):
    return (multiplicator * initial_seed + increment) % module


def generate_sequence_numbers_base(m, a, c, x0, n):
    secuencia = []
    xi = generate_number_base(m, a, c, x0)
    secuencia.append(xi)
    for num in range(n-1):
        xi = generate_number_base(m, a, c, xi)
        secuencia.append(xi)
    return secuencia


m = 2**24
a = 1140671485
c = 12820163


def generate_number(initial_seed):
    return generate_number_base(m, a, c, initial_seed)


def generate_sequence_numbers(n, initial_seed):
    arr = generate_sequence_numbers_base(m, a, c, initial_seed, n)
    return np.divide(arr, m)

# print(generate_sequence_numbers(10, 1337))


# ----------------- Generador RANDU -----------------

def randu(seed,n):
  values = np.empty(n)
  final_values = np.empty(n)
  values[0] = seed
  final_values[0] = values[0] / (2 ** 31 - 1)
  for i in range(1, n):
      values[i] = ((2 ** 16 + 3) * values[i - 1]) % (2 ** 31)
      final_values[i] = values[i] / (2 ** 31 )
  return final_values



# *****************************************************************
# ******************* TESTS DE EVALUACION *************************
# *****************************************************************


# TEST DE MAPA DE BITS

def bitmap_of_array(arr, title):
    matrix = []
    fila_aux = []
    lado = int(math.sqrt(len(arr)))
    for i in range(lado):
        for j in range(lado):
            if arr[lado * i + j] < 0.5:
                fila_aux.append(0)
            else:
                fila_aux.append(1)
        matrix.append(fila_aux)
        fila_aux = []

    fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)

    cmap = plt.cm.binary
    plt.imshow(matrix, cmap=cmap)
    plt.axis('off')
    plt.title(title)
    plt.show()

# ----------------------------------------------------------------

lado_bitmap = 1000

# Test GCL
bitmap_of_array(generate_sequence_numbers(lado_bitmap**2, 742895), 'GCL')

# Test MCM
bitmap_of_array(mid_square(6568, lado_bitmap**2), "MCM")

# Test Randu
bitmap_of_array(randu(1253, lado_bitmap**2), 'Randu')

# Test Python
arr = []
for _ in range(lado_bitmap**2):
    arr.append(random.random())
bitmap_of_array(arr, 'Generador de python3')


# TEST DE CHI-CUADRADO

def chi_squared_test(data, num_bins):
    observed, bins = np.histogram(data, bins=num_bins)
    expected = np.ones(num_bins) * len(data) / num_bins
    _, p_value = chisquare(observed, expected)
    return p_value

# Test GCL
seq_gcl = generate_sequence_numbers(1000, 742895)
p_gcl = chi_squared_test(seq_gcl, 10)
print('Valor de p para secuencia generada con GLC: ', p_gcl)

# Test MCM
seq_mcm = mid_square_no_div(9731, 100)
p_mcm = chi_squared_test(seq_mcm, 10)
print('Valor de p para secuencia generada con MCM: ', p_mcm)

# Test Randu
seq_randu = randu(1253,1000);
p_randu = chi_squared_test(seq_randu, 10)
print('Valor de p para secuencia generada con Randu: ', p_randu)

# Test Python
seq_python = [];
for _ in range(1000):
    seq_python.append(random.random())
p_python = chi_squared_test(seq_python, 10)
print('Valor de p para secuencia generada con Python3: ', p_python)


# Plot
labels = ['GCL', 'MCM', 'Randu', 'Python3']
p_values = [p_gcl, p_mcm, p_randu, p_python]

for i, v in enumerate(p_values):
    plt.text(i-0.1, v+0.01, str(round(v, 4)), fontsize=8)

plt.bar(labels, p_values)
plt.ylabel('Valor de p')
plt.title('Test de chi cuadrado')
plt.show()



# TEST KOLMOGOROV-SMIRNOV

def kolmogorov_smirnov_test(seq, gen_name):
    n = len(seq)
    seq.sort()
    dist = uniform(loc=0, scale=1)
    ecdf = np.arange(1, n + 1) / n
    tcdf = dist.cdf(seq)
    d = np.max(np.abs(ecdf - tcdf))
    alpha = 0.05
    critical_value = np.sqrt(-0.5 * np.log(alpha / 2)) / np.sqrt(n)
    
    if d < critical_value:
        print(f"{gen_name} pasó el test de Kolmogorov-Smirnov")
    else:
        print(f"{gen_name} falló el test de Kolmogorov-Smirnov")

    plt.plot(seq, ecdf, label="Función de distribución empírica")
    plt.plot(seq, tcdf, label="Función de distribución teórica")
    plt.xlabel('Valores ordenados de la secuencia')
    plt.ylabel('Probabilidad')
    plt.title('Test de Kolmogorov-Smirnov para el generador {}'.format(gen_name))
    plt.legend()
    plt.show()

# Test GCL
seq_gcl = generate_sequence_numbers(1000, 742895)
kolmogorov_smirnov_test(seq_gcl, "GCL")

# Test MCM
seq_mcm = mid_square(6568, 1000)
kolmogorov_smirnov_test(seq_mcm, "MCM")

# Test Randu
seq_randu = randu(1253, 1000)
kolmogorov_smirnov_test(seq_randu, "Randu")

# Test Python
seq_python = []
for _ in range(1000):
    seq_python.append(random.random())
kolmogorov_smirnov_test(seq_python, "Python3")



# TEST SUM OVERLAPPING

n=1000

# Test GCL
sumas = []
window= 50
step= 20
inf=0
sup=50
seed=742895
seq = generate_sequence_numbers(n, seed)
while(sup<=1000):
    acumulador = 0
    for n in range(inf, sup+1):
        acumulador+= seq[n]
    sumas.append(acumulador)
    inf+=step
    sup+=step
sumas.sort()
media = np.average(sumas)
std=np.std(sumas)
z= (max(sumas)-media)/std
plt.plot(sumas, scipy.stats.norm.pdf(sumas, media, std), color='red', linewidth=3 )
plt.title('Test superposicion de la suma - Generador GCL')
plt.show()


# Test MCM
sumas = []
window= 50
step= 20
inf=0
sup=50
seed=1232
seq = mid_square(seed,1000)
while(sup<=1000):
    acumulador = 0
    for n in range(inf, sup+1):
        acumulador+= seq[n]
    sumas.append(acumulador)
    inf+=step
    sup+=step
sumas.sort()
media = np.average(sumas)
std=np.std(sumas)
z= (max(sumas)-media)/std
plt.plot(sumas, scipy.stats.norm.pdf(sumas, media, std), color='red', linewidth=3 )
plt.title('Test superposicion de la suma - Generador MCM')
plt.show()

# Test Randu
sumas = []
window= 50
step= 20
inf=0
sup=50
seed=1232
seq = randu(1253,1000);
while(sup<=1000):
    acumulador = 0
    for n in range(inf, sup+1):
        acumulador+= seq[n]
    sumas.append(acumulador)
    inf+=step
    sup+=step
sumas.sort()
media = np.average(sumas)
std=np.std(sumas)
z= (max(sumas)-media)/std
plt.plot(sumas, scipy.stats.norm.pdf(sumas, media, std), color='red', linewidth=3 )
plt.title('Test superposicion de la suma - Generador Randu')
plt.show()

# Test Python

sumas = []
window= 50
step= 20
inf=0
sup=50
seq = []
for _ in range(1000):
    seq.append(random.random())
while(sup<=1000):
    acumulador = 0
    for n in range(inf, sup+1):
        acumulador+= seq[n]
    sumas.append(acumulador)
    inf+=step
    sup+=step
sumas.sort()
media = np.average(sumas)
std=np.std(sumas)
z= (max(sumas)-media)/std
plt.plot(sumas, scipy.stats.norm.pdf(sumas, media, std), color='red', linewidth=3 )
plt.title('Test superposicion de la suma - Generador Python')
plt.show()


## Para concluir que la distrubución es uniforme habrá que comprobar si el valor de Z está entre [-1.95, 1.95]