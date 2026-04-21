import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

# ==============================
# CONFIGURACIÓN
# ==============================

TAMANO = 1000
DIAS = 365

PROB_CONTAGIO = 0.25
PROB_RECUPERACION = 0.05
PROB_MUERTE = 0.01

SUSCEPTIBLE = 0
INFECTADO = 1
RECUPERADO = 2
MUERTO = 3

NUM_THREADS = multiprocessing.cpu_count()

# CREAR GRILLA

grilla = np.zeros((TAMANO, TAMANO), dtype=int)
grilla[TAMANO//2, TAMANO//2] = INFECTADO

# ==============================
# COLORES
# ==============================

colores = [
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, 1],
    [1, 1, 0]
]

os.makedirs("frames_paralelo", exist_ok=True)

datos = []
infectados_acumulados = 1


# ==============================
# FUNCIÓN THREAD
# ==============================

def procesar_bloque(inicio, fin, grilla, nueva_grilla):

    susceptibles = 0
    infectados = 0
    recuperados = 0
    muertos = 0

    for i in range(inicio, fin):
        for j in range(1, TAMANO - 1):

            estado = grilla[i, j]

            if estado == INFECTADO:

                vecinos = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]

                for x, y in vecinos:
                    if grilla[x, y] == SUSCEPTIBLE:
                        if np.random.rand() < PROB_CONTAGIO:
                            nueva_grilla[x, y] = INFECTADO

                if np.random.rand() < PROB_RECUPERACION:
                    nueva_grilla[i, j] = RECUPERADO

                elif np.random.rand() < PROB_MUERTE:
                    nueva_grilla[i, j] = MUERTO

    # Contar estadísticas locales
    bloque = nueva_grilla[inicio:fin]

    susceptibles = np.sum(bloque == SUSCEPTIBLE)
    infectados = np.sum(bloque == INFECTADO)
    recuperados = np.sum(bloque == RECUPERADO)
    muertos = np.sum(bloque == MUERTO)

    return susceptibles, infectados, recuperados, muertos


# ==============================
# SIMULACIÓN PARALELA
# ==============================

inicio = time.time()
frames = []

for dia in range(DIAS):

    nueva_grilla = grilla.copy()

    bloque = TAMANO // NUM_THREADS

    resultados = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:

        futures = []

        for t in range(NUM_THREADS):

            inicio_bloque = t * bloque
            fin_bloque = (t + 1) * bloque

            futures.append(
                executor.submit(
                    procesar_bloque,
                    inicio_bloque,
                    fin_bloque,
                    grilla,
                    nueva_grilla
                )
            )

        for f in futures:
            resultados.append(f.result())

    grilla = nueva_grilla

    # ==============================
    # REDUCCIÓN PARALELA
    # ==============================

    susceptibles = sum(r[0] for r in resultados)
    infectados = sum(r[1] for r in resultados)
    recuperados = sum(r[2] for r in resultados)
    muertos = sum(r[3] for r in resultados)

    if dia == 0:
        infectados_antes = 1
    else:
        infectados_antes = datos[-1][2]

    nuevos_infectados = infectados - infectados_antes
    infectados_acumulados += max(0, nuevos_infectados)

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

    # ==============================
    # IMAGEN
    # ==============================

    imagen = np.zeros((TAMANO, TAMANO, 3))

    for estado, color in enumerate(colores):
        imagen[grilla == estado] = color

    nombre = f"frames_paralelo/dia_{dia}.png"
    plt.imsave(nombre, imagen)

    frames.append(nombre)

    print(f"Dia {dia} paralelo | Infectados: {infectados}")

fin = time.time()

print("Tiempo Paralelo:", fin - inicio)

# ==============================
# CSV
# ==============================

df = pd.DataFrame(datos, columns=[
    "Dia",
    "Susceptibles",
    "Infectados",
    "Recuperados",
    "Muertos",
    "Infectados_Acumulados",
    "R0"
])

df.to_csv("estadisticas_paralelo.csv", index=False)

print("CSV generado")

# ==============================
# GIF
# ==============================

imagenes = []

for frame in frames:
    imagenes.append(imageio.imread(frame))

imageio.mimsave("simulacion_paralelo.gif", imagenes, fps=10)

print("GIF paralelo generado")