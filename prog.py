import random
import matplotlib.pyplot as plt

tamaño_poblacion = 50
n=7
numero_generaciones = 10000
poblacion = []
tasa_mutacion = 1
pathGuardarGrafico = "grafico10.png"

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
    #Calculamos la suma de las filas
    suma_filas = []
    for fila in dividir_Arreglo(individuo):
        suma_filas.append(sum(fila))
    if len(set(suma_filas)) != 1:
        errores += 1
    #Calculamos la suma de las columnas
    suma_columnas = []
    for i in range(n):
        suma_columnas.append(sum([fila[i] for fila in dividir_Arreglo(individuo)]))
    if len(set(suma_columnas)) != 1:
        errores += 1
    #Calculamos la suma de las diagonales
    suma_diagonal1 = sum([fila[i] for i, fila in enumerate(dividir_Arreglo(individuo))])
    suma_diagonal2 = sum([fila[-i-1] for i, fila in enumerate(dividir_Arreglo(individuo))])
    if suma_diagonal1 != suma_diagonal2:
        errores += 1
    #Verificamos que la suma de las diagonales sea igual a la suma de las filas y columnas
    if len(set([suma_diagonal1, suma_diagonal2] + suma_filas + suma_columnas)) != 1:
        errores += 1
    return errores

def inicializar_poblacion():
    for i in range(tamaño_poblacion):
        individuo = crear_Individuo(n)
        poblacion.append(individuo)
    return poblacion

def inicializar_poblacionDefault():
    for i in range(tamaño_poblacion):
        # Creamos un individuo de forma aleatoria utilizando el método que hemos definido anteriormente
        #individuo = [8, 1, 6, 3, 5, 7, 4, 9, 2]
        individuo = [2, 7, 6, 9, 5, 1, 4, 3, 8]
        # Añadimos el individuo a la población
        poblacion.append(individuo)
    return poblacion

def evaluar_poblacion():
    resultados = []
    for individuo in poblacion:
        errores = funcion_Aptitud(individuo)
        resultados.append(errores)
    return resultados

def seleccionar_individuo(resultados, n_individuos, poblacions):
    #emparejamos los resultados con los individuos
    individuos_resultados = list(zip(poblacions, resultados))
    #ordenamos los individuos de menor a mayor
    individuos_resultados.sort(key=lambda x: x[1])
    #seleccionamos los n individuos con menor error
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

#Iniciamos el programa
def main():
    x = []
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
        yMin.append(min(funcion_Aptitud(individuo) for individuo in poblacion))
        if calificacion == 0:
            break
    fig, ax = plt.subplots()
    ax.plot(x , yMax, color='red')
    ax.plot(x , yPro, color='blue')
    ax.plot(x , yMin, color='green')
    ax.set_title('Gráfica de aptitud')
    plt.savefig(pathGuardarGrafico);
if __name__ == "__main__":
    main()