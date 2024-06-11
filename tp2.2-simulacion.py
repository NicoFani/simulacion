import tp2_2_funciones as f
import os

op = 1;

while op != 0:
    os.system('cls' if os.name == 'nt' else 'clear')

    print("Menú:")
    print("1- Uniforme")
    print("2- Exponencial")
    print("3- Gamma")
    print("4- Normal")
    print("5- Pascal")
    print("6- Binomial")
    print("7- Hipergeométrica")
    print("8- Poisson")
    print("9- Empírica discreta")
    print("0- Salir")

    op = int(input("Ingrese el número de la opción deseada: "))

    os.system('cls' if os.name == 'nt' else 'clear')

    if op == 1:
        a = float(input("Ingrese el valor de a: "))
        b = float(input("Ingrese el valor de b: "))
        size = int(input("Ingrese la cantidad de valores a generar: "))
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Métodos:")
        print("1. Transformada Inversa")
        print("2. Rechazo y aceptación")
        method = int(input("Ingrese método a aplicar: "))
        if method == 1:
            f.uniforme_tf(a, b, size)
        elif method == 2:
            f.uniforme_mr(a, b, size)

    elif op == 2:
        lam = float(input("Ingrese valor de lamda: "))
        size = int(input("Ingrese la cantidad de valores a generar: "))
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Métodos:")
        print("1. Transformada Inversa")
        print("2. Rechazo y aceptación")
        method = int(input("Ingrese método a aplicar: "))
        if method == 1:
            f.exponencial_tf(lam, size)
        if method == 2:
            f.exponencial_mr(lam, size)

    elif op == 3:
        k = float(input("Ingrese valor de k: "))
        theta = float(input("Ingrese valor de theta: "))
        size = int(input("Ingrese la cantidad de valores a generar: "))
        f.gamma(k, theta, size)

    elif op == 4:
        media = float(input("Ingrese el valor de la media: "))
        sigma = float(input("Ingrese el valor de sigma: "))
        size = int(input("Ingrese la cantidad de valores a generar: "))
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Métodos:")
        print("1. Transformada Inversa")
        print("2. Rechazo y aceptación")
        method = int(input("Ingrese método a aplicar: "))
        if method == 1:
            f.normal_tf(media, sigma, size)
        if method == 2:
            f.normal_mr(media, sigma, size)

    elif op == 5:
        r = int(input("Ingrese el valor de la r (>0): "))
        p = float(input("Ingrese el valor de la p (entre 0 y 1): "))
        size = int(input("Ingrese la cantidad de valores a generar: "))
        f.pascal(r, p, size)

    elif op == 6:
        n = int(input("Ingrese el valor de la n: "))
        p = float(input("Ingrese el valor de p: "))
        size = int(input("Ingrese la cantidad de valores a generar: "))
        f.binomial(n, p, size)

    elif op == 7:
        N = int(input("Ingrese N: "))
        K = int(input("Ingrese K: "))
        n = int(input("Ingrese n: "))
        size = int(input("Ingrese la cantidad de valores a generar: "))
        f.hipergeometrica(N, K, n, size)

    elif op == 8:
        lam = float(input("Ingrese valor de lamda: "))
        size = int(input("Ingrese la cantidad de valores a generar: "))
        f.poisson_rechazo(lam, size)

    elif op == 9:
        size = int(input("Ingrese la cantidad de valores a generar: "))
        f.empirica_discreta(size)

    elif op == 0:
        print('Salida exitosa.')
        break

    else:
        print(
            "----------------------------- Opción inválida -----------------------------"
        )
        print("")
        input("Presione la tecla Enter para continuar...")