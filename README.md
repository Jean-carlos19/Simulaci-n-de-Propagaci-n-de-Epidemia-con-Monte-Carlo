# **Descripción del Proyecto**

Este proyecto consiste en la simulación de la propagación de una epidemia utilizando el método de Monte Carlo, comparando la ejecución secuencial con la ejecución paralela mediante el uso de Threads.
El objetivo principal es analizar el comportamiento de la propagación de una enfermedad dentro de una población simulada, además de evaluar la mejora en el tiempo de ejecución cuando se implementa paralelización.
Este proyecto fue desarrollado como parte de la asignatura de Programación Paralela, donde se busca aplicar conceptos como:
•	Programación Secuencial
•	Programación Paralela
•	Uso de Threads
•	Strong Scaling
•	Speed-Up
•	Visualización Animada
________________________________________
# Objetivos
Objetivo General
Simular la propagación de una epidemia utilizando el método Monte Carlo y comparar el rendimiento entre la ejecución secuencial y paralela.
Objetivos Específicos
•	Implementar simulación secuencial
•	Implementar simulación paralela con Threads
•	Medir tiempos de ejecución
•	Analizar speed-up
•	Generar visualización animada
•	Comparar resultados
________________________________________
# Tecnologías Utilizadas
•	Python
•	NumPy
•	Matplotlib
•	Threading
•	ImageIO
________________________________________

# Estructura del Proyecto
## **Simulacion-MonteCarlo/**
### Secuencial/
•	simulacion_secuencial.py
•	frames_secuencial/
### Paralelo/
•	simulacion_paralela.py
•	frames_paralelo/
### Resultados/
•	comparacion_animacion.py
•	strong_scaling.py
•	simulacion_comparacion.gif
________________________________________

# Cómo Ejecutar
Según la estructura del proyecto mostrada, los pasos para ejecutar correctamente la simulación son los siguientes:
1. Ejecutar Simulación Secuencial
Ubicarse en la carpeta principal del proyecto y ejecutar:
python secuencial/sir_secuencial.py
Esto generará:
•	Frames de simulación en frames_secuencial/
•	Archivo GIF simulacion_secuencial.gif
•	Archivo CSV con estadísticas
________________________________________

# 2. Ejecutar Simulación Paralela
### Ejecutar:
python paralelo/sir_paralelo.py
Esto generará:
•	Frames paralelos en frames_paralelo/
•	GIF simulacion_paralela.gif
•	Estadísticas paralelas en CSV
________________________________________
### 3. Ejecutar Strong Scaling
Para medir el rendimiento con múltiples Threads:
python paralelo/strong_scaly.py
Esto generará:
•	tiempos_scaling.csv
•	grafica_speedup.png
________________________________________
### 4. Generar Comparación Side by Side
Ejecutar:
python resultados/comparacion.py
Esto generará:
•	comparacion_animacion.gif
Esta animación muestra la simulación secuencial y paralela lado a lado.
________________________________________
### 5. Archivos Generados
Después de ejecutar todo el proyecto se generarán los siguientes archivos:
•	simulacion_secuencial.gif
•	simulacion_paralela.gif
•	comparacion_animacion.gif
•	grafica_speedup.png
•	tiempos_scaling.csv
•	estadisticas_secuencial.csv
•	estadisticas_paralelo.csv
________________________________________
### Estados de la Simulación
Durante la simulación cada individuo puede encontrarse en uno de los siguientes estados:
•	Susceptible (Verde)
•	Infectado (Rojo)
•	Muerto (Amarillo)
________________________________________
### Modelo de Simulación
La simulación se basa en una grilla donde cada celda representa un individuo.
Cada individuo puede:
•	Infectarse
•	Permanecer sano
•	Morir
