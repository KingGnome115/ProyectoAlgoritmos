import random
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

tamaño_poblacion = 50
n=6
numero_generaciones = 10000
poblacion = []
tasa_mutacion = 0.6
pathGuardarGrafico = "grafico10.png"
pathGuardarGraficoTiempo = "graficoT10.png"

def crear_Individuo(n):
    individuo = []
    for i in range(n**2):
        individuo.append(random.randint(1,n**2))
    return individuo

def dividir_Arreglo(arreglo):
    arreglo_dividido = []
    for i in range(0, len(arreglo), n):
        arreglo_dividido.append(arreglo[i:i+n])
    return arreglo_dividido

def funcion_Aptitud(individuo):
    errores = 0
    suma_filas = []
    for fila in dividir_Arreglo(individuo):
        suma_filas.append(sum(fila))
    if len(set(suma_filas)) != 1:
        errores += 1
    suma_columnas = []
    for i in range(n):
        suma_columnas.append(sum([fila[i] for fila in dividir_Arreglo(individuo)]))
    if len(set(suma_columnas)) != 1:
        errores += 1
    suma_diagonal1 = sum([fila[i] for i, fila in enumerate(dividir_Arreglo(individuo))])
    suma_diagonal2 = sum([fila[-i-1] for i, fila in enumerate(dividir_Arreglo(individuo))])
    if suma_diagonal1 != suma_diagonal2:
        errores += 1
    if len(set([suma_diagonal1, suma_diagonal2] + suma_filas + suma_columnas)) != 1:
        errores += 1
    return errores

def inicializar_poblacion():
    for i in range(tamaño_poblacion):
        individuo = crear_Individuo(n)
        poblacion.append(individuo)
    return poblacion

def evaluar_poblacion():
    resultados = []
    for individuo in poblacion:
        errores = funcion_Aptitud(individuo)
        resultados.append(errores)
    return resultados

def seleccionar_individuo(resultados, n_individuos, poblacions):
    individuos_resultados = list(zip(poblacions, resultados))
    individuos_resultados.sort(key=lambda x: x[1])
    individuos_seleccionados = [individuo[0] for individuo in individuos_resultados[:n_individuos]]
    return individuos_seleccionados

def reproducir(individuo1, individuo2):
    punto_corte = random.randint(1, len(individuo1)-1)
    hijo1 = individuo1[:punto_corte] + individuo2[punto_corte:]
    hijo2 = individuo2[:punto_corte] + individuo1[punto_corte:]
    return hijo1, hijo2

def mutar(individuo):
    if random.random() < tasa_mutacion:
        posicion1 = random.randint(0, len(individuo)-1)
        posicion2 = random.randint(0, len(individuo)-1)
        while posicion1 == posicion2:
            posicion2 = random.randint(0, len(individuo)-1)
        individuo[posicion1], individuo[posicion2] = individuo[posicion2], individuo[posicion1]
    return individuo

def reproducir_mutar(individuos_seleccionados):
    nueva_generacion = []
    for i in range(0, len(individuos_seleccionados)):
        individuo1 = individuos_seleccionados[i]
        if i+1 < len(individuos_seleccionados):
            individuo2 = individuos_seleccionados[i+1]
        else:
            individuo2 = individuos_seleccionados[0]
        hijo1, hijo2 = reproducir(individuo1, individuo2)
        nueva_generacion.append(hijo1)
        nueva_generacion.append(hijo2)
    for individuo in range(len(nueva_generacion)):
        nueva_generacion[individuo] = mutar(nueva_generacion[individuo])
    return nueva_generacion

def main():
    x = []
    y = []
    yMax = []
    yPro = []
    yMin = []
    poblacion = inicializar_poblacion()
    print("Población inicial: ", poblacion)
    print("Tamaño de la población: ", len(poblacion))
    print("Tamaño de cuadro mágico: ", n)
    print("Numero de generaciones: ", numero_generaciones)
    print("Tasa de mutación: ", tasa_mutacion)
    print("\n")
    for i in range(numero_generaciones):
        start_time = time.time()
        resultados = evaluar_poblacion()
        individuos_seleccionados = seleccionar_individuo(resultados, (tamaño_poblacion//2)+1, poblacion)
        poblacion = reproducir_mutar(individuos_seleccionados)
        calificacion = funcion_Aptitud(individuos_seleccionados[0])
        print("Generación: ", i)
        x.append(i)
        print("Mejor individuo: ", individuos_seleccionados[0])
        print("Calificación del mejor individuo: ", calificacion)
        cuboMagico = dividir_Arreglo(individuos_seleccionados[0])
        for fila in cuboMagico:
            print(fila)
        print("\n")
        yMax.append(max(funcion_Aptitud(individuo) for individuo in poblacion))
        yPro.append(sum(funcion_Aptitud(individuo) for individuo in poblacion)/len(poblacion))
        mini = (min(funcion_Aptitud(individuo) for individuo in poblacion))
        if(mini == 0):
            mini = 1
        yMin.append(mini)
        elapsed_time = time.time() - start_time
        y.append(elapsed_time)
        if calificacion == 0:
            break
    fig, ax = plt.subplots()
    ax.plot(x , yMax, color='red')
    ax.plot(x , yPro, color='blue')
    ax.plot(x , yMin, color='green')
    ax.set_title('Gráfica de aptitud')
    #Agregar signifcado a los colores
    red_patch = mpatches.Patch(color='red', label='Máximo')
    blue_patch = mpatches.Patch(color='blue', label='Promedio')
    green_patch = mpatches.Patch(color='green', label='Mínimo')
    plt.legend(handles=[red_patch, blue_patch, green_patch])


    plt.savefig(pathGuardarGrafico);

    fig, ax = plt.subplots()
    ax.plot(x , y, color='red')
    ax.set_title('Gráfica de tiempo')
    plt.savefig(pathGuardarGraficoTiempo);

if __name__ == "__main__":
    main()