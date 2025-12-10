import numpy as np
from .perlin_base import dot_product, lerp, fade

# ----------------------------------------------------------------------
#  Clase PerlinNoiseGenerator: 
#  para no estar pasando arrays muy grandes o  usarvariables globales.
#  TIENE:
#  el estado (gradientes) 
#  metodo para generar el ruido. 
# -----------------------------------------------------------------------------

class PerlinNoiseGenerator:
    
    def __init__(self, tam_grid_x, tam_grid_y, seed=None):
        """Inicializa la grilla de gradientes."""
        self.TAM_GRID_X = tam_grid_x
        self.TAM_GRID_Y = tam_grid_y
        
        if seed is not None:
            np.random.seed(seed)
            
        self.gradients = self._initialize_gradients()
        
    def _initialize_gradients(self):
        """Crea y llena la grilla con vectores aleatorios unitarios."""
        gradients = np.zeros((self.TAM_GRID_X, self.TAM_GRID_Y, 2))
        for i in range(self.TAM_GRID_X):
            for j in range(self.TAM_GRID_Y):
                # angulo aleatorio 
                angle = np.random.uniform(0, 2 * np.pi)
                gradients[i, j] = np.array([np.cos(angle), np.sin(angle)])
        return gradients

    # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # -
    #  FUNCIONES PARA CALCULAR EL RUIDO
    #  perlin clasico / contribucion_sw
    # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # -

    def perlin_clasico(self, x, y, alpha=1.0):
        """Función de Ruido Perlin completa (con fade)"""
        scaled_x = x * alpha; scaled_y = y * alpha
        x0 = int(np.floor(scaled_x)); y0 = int(np.floor(scaled_y))
        xf = scaled_x - x0; yf = scaled_y - y0
        x1 = x0 + 1; y1 = y0 + 1
        
        # comprobacion de limites (usa self.TAM_GRID_X/Y)
        if x1 >= self.TAM_GRID_X or y1 >= self.TAM_GRID_Y or x0 < 0 or y0 < 0:
            return 0.0

        # gradientes de las 4 esquinas
        g00 = self.gradients[x0, y0]; g10 = self.gradients[x1, y0]
        g01 = self.gradients[x0, y1]; g11 = self.gradients[x1, y1]
        
        # vectores distancia
        d00 = np.array([xf, yf]); d10 = np.array([xf - 1, yf])
        d01 = np.array([xf, yf - 1]); d11 = np.array([xf - 1, yf - 1])
        
        # calculamos los cuatro productos punto
        n00 = dot_product(g00, d00); n10 = dot_product(g10, d10)
        n01 = dot_product(g01, d01); n11 = dot_product(g11, d11)
        
        # suavizado 
        u = fade(xf); v = fade(yf)
        
        # doble interpolación
        nx0 = lerp(n00, n10, u); nx1 = lerp(n01, n11, u)
        final_noise = lerp(nx0, nx1, v)
        
        return final_noise


    def perlin_contribucion_sw(self, x, y, alpha=1.0):
        """Calcula solo la contribución del producto punto del nodo de la esquina sw."""
        scaled_x = x * alpha; scaled_y = y * alpha
        x0 = int(np.floor(scaled_x)); y0 = int(np.floor(scaled_y))
        xf = scaled_x - x0; yf = scaled_y - y0
        
        if x0 >= self.TAM_GRID_X or y0 >= self.TAM_GRID_Y or x0 < 0 or y0 < 0:
            return 0.0

        g00 = self.gradients[x0, y0]
        d00 = np.array([xf, yf])
        
        return dot_product(g00, d00)


    def perlin_linear(self, x, y, alpha=1.0):
        """Ruido Perlin usando interpolación lineal (sin fade)."""
        scaled_x = x * alpha; scaled_y = y * alpha
        x0 = int(np.floor(scaled_x)); y0 = int(np.floor(scaled_y))
        xf = scaled_x - x0; yf = scaled_y - y0
        x1 = x0 + 1; y1 = y0 + 1
        
        if x1 >= self.TAM_GRID_X or y1 >= self.TAM_GRID_Y or x0 < 0 or y0 < 0:
            return 0.0
        
        g00 = self.gradients[x0, y0]; g10 = self.gradients[x1, y0]
        g01 = self.gradients[x0, y1]; g11 = self.gradients[x1, y1]
        
        d00 = np.array([xf, yf]); d10 = np.array([xf - 1, yf])
        d01 = np.array([xf, yf - 1]); d11 = np.array([xf - 1, yf - 1])
        
        n00 = dot_product(g00, d00); n10 = dot_product(g10, d10)
        n01 = dot_product(g01, d01); n11 = dot_product(g11, d11)
        
        u = xf; v = yf # Usamos coordenadas fraccionarias para lerp
        
        nx0 = lerp(n00, n10, u); nx1 = lerp(n01, n11, u)
        return lerp(nx0, nx1, v)


    def perlin_promedio(self, x, y, alpha = 1.0):
        """Promedio de los cuatro productos punto (sin interpolacion)."""
        scaled_x = x * alpha; scaled_y = y * alpha
        x0 = int(np.floor(scaled_x)); y0 = int(np.floor(scaled_y))
        xf = scaled_x - x0; yf = scaled_y - y0
        x1 = x0 + 1; y1 = y0 + 1
        
        if x1 >= self.TAM_GRID_X or y1 >= self.TAM_GRID_Y or x0 < 0 or y0 < 0:
            return 0.0
        
        g00 = self.gradients[x0, y0]; g10 = self.gradients[x1, y0]
        g01 = self.gradients[x0, y1]; g11 = self.gradients[x1, y1]
        
        d00 = np.array([xf, yf]); d10 = np.array([xf - 1, yf])
        d01 = np.array([xf, yf - 1]); d11 = np.array([xf - 1, yf - 1])
        
        n00 = dot_product(g00, d00); n10 = dot_product(g10, d10)
        n01 = dot_product(g01, d01); n11 = dot_product(g11, d11)
        
        average_value = (n00 + n10 + n01 + n11) / 4.0
        
        return average_value