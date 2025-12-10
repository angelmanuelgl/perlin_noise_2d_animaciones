import numpy as np

# ------------------------------------------------------
# Funciones Auxiliares (Ken Perlin)
# ------------------------------------------------------

# funcion de suavizado de Ken Perlin f(t) = 6t^5 - 15t^4 + 10t^3
def fade(t):
    return 6 * t**5 - 15 * t**4 + 10 * t**3

# interpolacion lineal ntre a y b usando el peso t
def lerp(a, b, t):
    return a + t * (b - a)

# producto punto de gradiente y vector distancia
def dot_product(g, d):
    return g[0] * d[0] + g[1] * d[1]
