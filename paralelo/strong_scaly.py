import os
os.makedirs("../Resultados", exist_ok=True)

import numpy as np
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# ==============================
# CONFIGURACION
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


def procesar_bloque(inicio, fin, grilla, nueva_grilla):

    for i in range(inicio, fin):
        for j in range(1, TAMANO-1):

            if grilla[i, j] == INFECTADO:

                vecinos = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]

                for x, y in vecinos:
                    if grilla[x, y] == SUSCEPTIBLE:
                        if np.random.rand() < PROB_CONTAGIO:
                            nueva_grilla[x, y] = INFECTADO

                if np.random.rand() < PROB_RECUPERACION:
                    nueva_grilla[i, j] = RECUPERADO

                elif np.random.rand() < PROB_MUERTE:
                    nueva_grilla[i, j] = MUERTO


def ejecutar_simulacion(num_threads):

    grilla = np.zeros((TAMANO, TAMANO), dtype=int)
    grilla[TAMANO//2, TAMANO//2] = INFECTADO

    inicio = time.time()

    for dia in range(DIAS):

        nueva_grilla = grilla.copy()

        bloque = TAMANO // num_threads

        with ThreadPoolExecutor(max_workers=num_threads) as executor:

            futures = []

            for t in range(num_threads):

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
                f.result()

        grilla = nueva_grilla

    fin = time.time()

    return fin - inicio


# ==============================
# EXPERIMENTOS
# ==============================

threads = [1, 2, 4, 8]
tiempos = []

for t in threads:

    print(f"Ejecutando con {t} threads...")

    tiempo = ejecutar_simulacion(t)

    tiempos.append(tiempo)

    print(f"Tiempo: {tiempo}")


# ==============================
# SPEEDUP
# ==============================

tiempo_base = tiempos[0]

speedup = [tiempo_base / t for t in tiempos]

# ==============================
# CSV
# ==============================

df = pd.DataFrame({
    "Threads": threads,
    "Tiempo": tiempos,
    "Speedup": speedup
})

df.to_csv("tiempos_scaling.csv", index=False)

print("CSV generado")

# ==============================
# GRAFICA
# ==============================

plt.figure()

plt.plot(threads, speedup, marker="o")

plt.xlabel("Numero de Threads")
plt.ylabel("Speedup")

plt.title("Strong Scaling - Simulacion Epidemia")

plt.savefig("grafica_speedup.png")

print("Grafica generada")