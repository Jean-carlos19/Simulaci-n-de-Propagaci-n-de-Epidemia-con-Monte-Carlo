import imageio
import numpy as np
import os
import matplotlib.pyplot as plt

carpeta_secuencial = "secuencial/frames_secuencial"
carpeta_paralelo = "paralelo/frames_paralelo"

frames_secuencial = sorted(os.listdir(carpeta_secuencial))
frames_paralelo = sorted(os.listdir(carpeta_paralelo))

imagenes_finales = []

print("Creando animación profesional...")

for i, (f_sec, f_par) in enumerate(zip(frames_secuencial, frames_paralelo)):

    img_sec = imageio.imread(os.path.join(carpeta_secuencial, f_sec))
    img_par = imageio.imread(os.path.join(carpeta_paralelo, f_par))

    fig, axs = plt.subplots(1, 2, figsize=(12,5))

    axs[0].imshow(img_sec)
    axs[0].set_title("Simulación Secuencial", fontsize=14)
    axs[0].axis("off")

    axs[1].imshow(img_par)
    axs[1].set_title("Simulación Paralela", fontsize=14)
    axs[1].axis("off")

    plt.suptitle(f"Comparación Monte Carlo - Iteración {i}", fontsize=16)

    # Leyenda
    leyenda = [
        plt.Line2D([0],[0], marker='s', color='w', label='Susceptible',
                   markerfacecolor='green', markersize=10),

        plt.Line2D([0],[0], marker='s', color='w', label='Infectado',
                   markerfacecolor='red', markersize=10),

        plt.Line2D([0],[0], marker='s', color='w', label='Muerto',
                   markerfacecolor='yellow', markersize=10)
    ]

    fig.legend(handles=leyenda, loc="lower center", ncol=3)

    fig.canvas.draw()

    fig.canvas.draw()

    image = np.array(fig.canvas.renderer.buffer_rgba())

    imagenes_finales.append(image)

    plt.close()

    imagenes_finales.append(image)

    plt.close()

imageio.mimsave("simulacion_comparacion.gif", imagenes_finales, fps=8)

print("Animación profesional creada")