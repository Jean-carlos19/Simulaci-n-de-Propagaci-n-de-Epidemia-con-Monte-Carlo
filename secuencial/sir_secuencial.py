import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import time
import pandas as pd


# CONFIGURACIÓN

TAMANO = 1000   # 1000 x 1000
DIAS = 365

PROB_CONTAGIO = 0.25
PROB_RECUPERACION = 0.05
PROB_MUERTE = 0.01

# Estados
SUSCEPTIBLE = 0
INFECTADO = 1
RECUPERADO = 2
MUERTO = 3


# VALIDACIÓN CASO PEQUEÑO

VALIDACION = True # Cambiar a True para probar 100x100

if VALIDACION:
    TAMANO = 100
    DIAS = 50

#CREACION GRILLA

grilla = np.zeros((TAMANO, TAMANO), dtype=int)

# Infectar persona inicial
grilla[TAMANO//2, TAMANO//2] = INFECTADO



# COLORES

colores = [
    [0, 1, 0],   # Verde - Susceptible
    [1, 0, 0],   # Rojo - Infectado
    [0, 0, 1],   # Azul - Recuperado
    [1, 1, 0]    # Amarillo - Muerto
]


# CREAR CARPETAS

os.makedirs("frames_secuencial", exist_ok=True)


# ESTADÍSTICAS


datos = []

infectados_acumulados = 1


# SIMULACIÓN


inicio = time.time()

frames = []

for dia in range(DIAS):

    nueva_grilla = grilla.copy()

    infectados_antes = np.sum(grilla == INFECTADO)

    for i in range(1, TAMANO - 1):
        for j in range(1, TAMANO - 1):

            if grilla[i, j] == INFECTADO:

                # Contagio vecinos
                vecinos = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]

                for x, y in vecinos:
                    if grilla[x, y] == SUSCEPTIBLE:
                        if np.random.rand() < PROB_CONTAGIO:
                            nueva_grilla[x, y] = INFECTADO

                # Recuperación
                if np.random.rand() < PROB_RECUPERACION:
                    nueva_grilla[i, j] = RECUPERADO

                # Muerte
                elif np.random.rand() < PROB_MUERTE:
                    nueva_grilla[i, j] = MUERTO

    grilla = nueva_grilla


# ESTADÍSTICAS

    susceptibles = np.sum(grilla == SUSCEPTIBLE)
    infectados = np.sum(grilla == INFECTADO)
    recuperados = np.sum(grilla == RECUPERADO)
    muertos = np.sum(grilla == MUERTO)

    nuevos_infectados = infectados - infectados_antes

    infectados_acumulados += max(0, nuevos_infectados)

    # Calcular R0
    if infectados_antes > 0:
        r0 = nuevos_infectados / infectados_antes
    else:
        r0 = 0

    datos.append([
        dia,
        susceptibles,
        infectados,
        recuperados,
        muertos,
        infectados_acumulados,
        r0
    ])


# CREACION DE IMAGEN

    imagen = np.zeros((TAMANO, TAMANO, 3))

    for estado, color in enumerate(colores):
        imagen[grilla == estado] = color

    nombre = f"frames_secuencial/dia_{dia}.png"
    plt.imsave(nombre, imagen)

    frames.append(nombre)

    print(f"Dia {dia} | Infectados: {infectados} | Muertos: {muertos}")

fin = time.time()

print("Tiempo Secuencial:", fin - inicio)


# GUARDAR CSV

df = pd.DataFrame(datos, columns=[
    "Dia",
    "Susceptibles",
    "Infectados",
    "Recuperados",
    "Muertos",
    "Infectados_Acumulados",
    "R0"
])

df.to_csv("estadisticas_secuencial.csv", index=False)

print("CSV generado")



# CREAR GIF


imagenes = []

for frame in frames:
    imagenes.append(imageio.imread(frame))

imageio.mimsave("simulacion_secuencial.gif", imagenes, fps=10)

print("GIF generado")