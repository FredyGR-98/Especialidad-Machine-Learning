# Importación de librería a utilizar
import numpy as np

# 1. Resolución de Sistemas de Ecuaciones Lineales:
# Declaración de matriz A tamaño 3x3
A = np.array([[3, -1, 2],[1, 2, 1],[2, 1, 3]], dtype=float)

# Declaración del vector b
b = np.array([5, 6, 7], dtype=float)

# Operación a realizar para conseguir el resultado correspondiente
print("Solucion del sistema \n",np.linalg.solve(A, b))

# Resultados: X = 2.0 ; Y = 1.8 ; Z = 0.4

# Mismo ejercicio pero tomando en consideración el Mínimo Común
x_lstsq, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
print("parametros beta usando lstsq \n ",x_lstsq)

# Resultados: X = 2.0 ; Y = 1.8 ; Z = 0.4
