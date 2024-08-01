import scipy.stats as stats
import scipy.special as sc
import scipy as scpy

import matplotlib.pyplot as plt
import numpy as np
import math as math
import msvcrt

# ----- Funciones para Metodo de Rechazo ------

def metodo_rechazo(pdf_estudio, techo, min, max, size):
    accepted = []
    for _ in range(size):
        x = np.random.uniform(min, max)
        prob_pass = pdf_estudio(x) / techo
        if (np.random.uniform(0, 1) <= prob_pass):
            accepted.append(x)
    return accepted


def metodo_rechazo_dicreto(mpf_estudio, techo, min, max, size):
    accepted = []
    for _ in range(size):
        x = np.random.uniform(min, max)
        x = round(x)
        prob_pass = mpf_estudio(x) / techo
        if (np.random.uniform(0, 1) <= prob_pass):
            accepted.append(x)
    return accepted


# ----- Función para Test Kolmogorov-Smirnov -----

def ks_test(seq, d_type, distr_name):
    d_positive = []
    d_negative = []
    seq.sort()

    for i in range(len(seq)):
        d_positive.append(i / len(seq) - seq[i])
        d_negative.append(seq[i] - (i - 1) / len(seq))
    
    d_max = max(max(d_positive), max(d_negative))
    
    if type(d_type) is type(stats.binom):
        k = stats.binom.ppf(1 - 0.05 / 2, len(seq), p = 0.5)
    elif type(d_type) is type(stats.nbinom):
        k = stats.nbinom.ppf(1 - 0.05 / 2, len(seq), p = 0.5)
    else:
        k = d_type.ppf(1 - 0.05 / 2, len(seq))

    print("\n\n" + "\033[4m" + "Resultado del test:" + "\033[0m")
    if d_max < k:
        print("La distribución", distr_name, "pasó la prueba.")
    else:
        print("La distribución", distr_name, "falló la prueba.")

    print("\n" + "Presione cualquier tecla para continuar...")
    msvcrt.getch()


# ----- Metodo de Rechazo -----

# Distribución Binomial

def mdf_binomial(n, p):
    factorial = lambda x: math.factorial(int(x))
    f1 = lambda x: factorial(n) / (factorial(x) * factorial(n - x))
    f2 = lambda x: (p**x) * ((1 - p)**(n - x))
    return lambda x: f1(x) * f2(x)

def binomial(n, p, size):
    name = "Binomial"
    min = 0
    max = n
    mdf = mdf_binomial(n, p)
    techo = 1

    accepted = metodo_rechazo_dicreto(mpf_estudio=mdf,
                                         techo=techo,
                                         min=min,
                                         max=max,
                                         size=size)

    fa = {}
    for i in accepted:
        fa[i] = fa.get(i, 0) + 1

    for k in fa.keys():
        fa[k] = fa[k] / len(accepted)

    plt.bar(fa.keys(), fa.values(), label=name + " por método rechazo")

    # Funcion teorica
    x = range(0, n)
    y = list(map(lambda k: mdf(k), x))
    plt.scatter(x, y, color='red', label=name + ' teorica')

    plt.title('Distribución ' + name+ f" / size={size} n={n} p={p}")
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()

    ks_test(accepted, stats.binom, "Binomial (rechazo)")

# Distribución Uniforme

def uniforme_pdf(a, b):
    return lambda x: 1 / (b - a)


def uniforme_mr(a, b, size):
    name = "Uniforme"
    min = a
    max = b
    pdf = uniforme_pdf(a, b)
    techo = pdf((a + b) / 2)

    accepted = metodo_rechazo(pdf_estudio=pdf,
                                 techo=techo,
                                 min=min,
                                 max=max,
                                 size=size)

    plt.hist(accepted,
             bins=30,
             density=True,
             label=name + " por método rechazo")

    # Funcion teorica
    x = np.linspace(min, max, size)
    y = [pdf(x)] * len(x)
    plt.plot(x, y, color='red', label=name + ' teorica')

    plt.title('Distribución ' + name + f" / size={size} a={a} b={b}")
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()

    ks_test(accepted, stats.uniform, "Uniforme (rechazo)")

# Distribución Poisson
    
fig, ax = plt.subplots()

accepted=[]
a=0
b=30

def fg(x, lam)->float:
    return (math.exp(-lam)*pow(lam, x))/(sc.factorial(x))

def fx(r)->float:
    return a+(b-a)*r

def poisson_rechazo(lam, size):
    for ran in range(10000):
        x=fx(np.random.uniform(0,1))
        g=fg(x, lam)
        rand=np.random.uniform(0,1)
        if(rand<=g):
            accepted.append(x)

    plt.hist(accepted,
            bins=30,
            density=True,
            label="Poisson por metodo rechazo")

    # Funcion teorica
    x = np.linspace(a, b, size)
    y = (math.exp(-lam)*pow(lam, x))/(sc.factorial(x))
    ax.plot(x, y, 'r-', linewidth=2)
    plt.plot(x, y, color='red', label='Poisson teórica')
    plt.title('Distribución Poisson' + f" / size={size} lamda={lam}")
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()

    ks_test(accepted, stats.poisson, "Poisson (rechazo)")

# Distribución Empírica Discreta

def mdf_empirica():

    def mdf(x):
        if x == 1:
            return 0.3
        elif x == 2:
            return 0.4
        elif x == 4:
            return 0.3
        else:
            return 0

    return mdf


def empirica_discreta(size):
    name = "Empirica discreta"
    min = 0
    max = 5
    mdf = mdf_empirica()
    techo = 0.4

    accepted = metodo_rechazo_dicreto(mpf_estudio=mdf,
                                         techo=techo,
                                         min=min,
                                         max=max,
                                         size=size)

    fa = {}
    for i in accepted:
        fa[i] = fa.get(i, 0) + 1

    for k in fa.keys():
        fa[k] = fa[k] / len(accepted)

    plt.bar(fa.keys(), fa.values(), label=name + " por método rechazo")

    # Funcion teorica
    x = range(0, max)
    y = list(map(lambda k: mdf(k), x))
    plt.scatter(x, y, color='red', label=name + ' teorica')

    plt.title('Distribución ' + name + f" / size={size}")
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()

    ks_test(accepted, stats.rv_discrete, "Empirica Discreta (rechazo)")
# Distribución Exponencial

def exponencial_mr(lam, size):
    name = "Exponencial"
    min = 0
    max = (-1 / lam) * np.log(1 - 0.999)
    pdf = lambda x: lam * np.exp(-lam * x)
    techo = lam

    accepted = metodo_rechazo(pdf_estudio=pdf,
                                 techo=techo,
                                 min=min,
                                 max=max,
                                 size=size)

    plt.hist(accepted,
             bins=30,
             density=True,
             label=name + " por método rechazo")

    # Funcion teorica
    x = np.linspace(min, max, size)
    y = pdf(x)
    plt.plot(x, y, color='red', label=name + ' teorica')

    plt.title('Distribución ' + name + f" / size={size} lamba={lam}")
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()

    ks_test(accepted, stats.expon, "Exponencial (rechazo)")

# Distribucion Gamma

def gamma_pdf(k, theta):
    factor_1 = 1 / (math.factorial(int(k) - 1) * (theta**k))
    factor_2 = lambda x: x**(k - 1)
    factor_3 = lambda x: np.exp(-x / theta)
    return lambda x: factor_1 * factor_2(x) * factor_3(x)


def gamma(k, theta, size):
    name = "Gamma"
    min = 0
    max = k * theta + 2 * k * theta**2  #aprox con la regla empirica
    pdf = gamma_pdf(k, theta)
    techo = pdf((k - 1) * theta)

    accepted = metodo_rechazo(pdf_estudio=pdf,
                                 techo=techo,
                                 min=min,
                                 max=max,
                                 size=size)

    plt.hist(accepted,
             bins=30,
             density=True,
             label=name + " por método rechazo")

    # Funcion teorica
    x = np.linspace(min, max, size)
    y = pdf(x)
    plt.plot(x, y, color='red', label=name + ' teorica')

    plt.title('Distribución ' + name + f" / size={size} theta={theta} k={k}")
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()


# Distribución Hiper-Geométrica

def hipergeometrica(N, K, n, size):
    name = "Hipergeometrica"
    rv = stats.hypergeom(N, K, n)

    x = np.arange(0, n+1)
    pmf_hypergeom = rv.pmf(x)

    def rechazo_hipergeometrica(N, K, n, num_samples):
        samples = []
        max_pmf = max(pmf_hypergeom)

        while len(samples) < num_samples:
            # Generar una muestra candidata de una distribución uniforme discreta
            candidate = np.random.randint(0, n+1)

            # Calcular la probabilidad de aceptar la candidata
            accept_prob = rv.pmf(candidate) / max_pmf

            # Generar un número aleatorio uniforme para la decisión de aceptación
            u = np.random.uniform()

            if u < accept_prob:
                samples.append(candidate)

        return samples

    # Generar muestras usando el método de rechazo
    samples = rechazo_hipergeometrica(N, K, n, size)

    plt.hist(samples, bins=np.arange(-0.5, n+1.5, 1), density=True, alpha=0.75, label='Muestras generadas')
    plt.plot(x, pmf_hypergeom, 'ro', label='Hipergeométrica PMF')  # Solo puntos, sin líneas
    plt.title('Distribución ' + name + f" - size={size} N={N} k={K} n={n}")
    plt.xlabel('Número de éxitos en la muestra')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.show()

# Distribución Normal

def normal_pdf(mean, sigma):
    coeficient = 1 / (sigma * np.sqrt(2 * np.pi))
    index = lambda x: -0.5 * ((x - mean) / sigma)**2
    return lambda x: coeficient * np.exp(index(x))


def normal_mr(mean, sigma, size):
    name = "Normal"
    min = mean - 3 * sigma
    max = mean + 3 * sigma
    pdf = normal_pdf(mean, sigma)
    techo = pdf(mean)

    accepted = metodo_rechazo(pdf_estudio=pdf,
                                 techo=techo,
                                 min=min,
                                 max=max,
                                 size=size)

    plt.hist(accepted,
             bins=30,
             density=True,
             label=name + " por método rechazo")

    # Funcion teorica
    x = np.linspace(min, max, size)
    y = pdf(x)
    plt.plot(x, y, color='red', label=name + ' teorica')

    plt.title('Distribución ' + name + f" / size={size} promedio={mean} desvio={sigma}")
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()

    ks_test(accepted, stats.norm, "Normal (rechazo)")

# Distribución de Pascal

def mdf_pascal(r, p):
    return lambda x: math.comb(x + r - 1, x) * (p**r) * ((1 - p)**x)


def pascal(r, p, size):
    name = "Pascal"
    moda = math.floor((r - 1) * (1 - p) / p)
    min = 0
    max = moda * 2
    mdf = mdf_pascal(r, p)
    techo = mdf(moda)

    accepted = metodo_rechazo_dicreto(mpf_estudio=mdf,
                                         techo=techo,
                                         min=min,
                                         max=max,
                                         size=size)

    fa = {}
    for i in accepted:
        fa[i] = fa.get(i, 0) + 1

    for k in fa.keys():
        fa[k] = fa[k] / len(accepted)

    plt.bar(fa.keys(), fa.values(), label=name + " por método rechazo")

    # Funcion teorica
    x = range(min, max)
    y = list(map(lambda k: mdf(k), x))
    plt.scatter(x, y, color='red', label=name + ' teorica')

    plt.title('Distribución ' + name + f" / size={size} r={r} p={p}")
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()


# ----- Metodo de la Transformada Inversa ------

# Distribución Exponencial

def exponencial_tf(lam, size):

    fig, ax = plt.subplots()

    # Distribucion generada a partir de la uniforme
    datos = np.random.uniform(0, 1, size)
    transform = np.vectorize(lambda u: (-1 / lam) * np.log(1 - u))
    datos = transform(datos)
    plt.hist(datos,
             bins=30,
             density=True,
             label="Exponencial por transformada inversa")

    # Funcion teorica
    x = np.linspace(0, np.amax(datos), 100)
    y = lam * np.exp(-lam * x)
    ax.plot(x, y, 'r-', linewidth=2)
    plt.plot(x, y, color='red', label='Exponencial teorica')

    plt.title('Distribución Exponencial')
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()

    ks_test(datos, stats.expon, "Exponencial (inversa)")

# Distribución Uniforme

def uniforme_tf(a, b, size):
    datos = np.random.uniform(a, b, size)

    # Valores de la función de densidad en un rango de valores de x
    x = np.linspace(a, b, 1000)
    y = np.full_like(x, 1 / (b - a))

    plt.plot(x, y, color='red', label='Distribución Uniforme')
    plt.hist(datos, bins=10, density=True)
    plt.legend(["Función de densidad de probabilidad"], loc='upper right')
    plt.title('Distribución Uniforme')
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.show()

    ks_test(datos, stats.uniform, "Uniforme (inversa)")


# Distribución Normal

def newton_raphson(p, mu=0, sigma=1, tol=1e-6, max_iter=100):
    x = mu # initial guess
    for i in range(max_iter):
        pdf = scpy.pdf(x, loc=mu, scale=sigma)
        cdf = scpy.cdf(x, loc=mu, scale=sigma)
        x_new = x - (cdf - p) / pdf
        if abs(x_new - x) < tol:
            break
        x = x_new
    return x

#f^(-1)(y) = μ ± σ√(-2ln(yσ√(2π)))

def normal_tf(media, sigma, size): 

    fig, ax = plt.subplots()
    #f(x) = (1 / σ√(2π)) * e^(-(x-μ)^2 / (2σ^2))
    #  
    # Distribucion generada a partir de la uniforme
    datos = np.random.uniform(0, 1, size)
    transformZ = np.vectorize(lambda u: (pow(u, 0.1349)-pow(1-u,0.1349))/0.1975)
    datosZ = transformZ(datos);
    transformX = np.vectorize(lambda u: u*sigma+media)
    datosX=transformX(datosZ)
    plt.hist(datosX,
            bins=30,
            density=True,
            label="Normal por transformada inversa")

    #Normal teórica
    x = np.linspace(media-3*sigma, media+3*sigma, size)
    y = (1/(sigma*np.sqrt(2*np.pi)))*(np.exp(-pow(x-media,2)/(2*pow(sigma,2))))
    ax.plot(x, y, 'r-', linewidth=2)
    plt.plot(x, y, color='red', label='Normal teórica')
    
    plt.title('Distribución Normal')
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad')
    plt.legend(["Función de densidad de probabilidad"], loc='upper right')
    plt.show()

    ks_test(datos, stats.norm, "Normal (inversa)")