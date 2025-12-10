import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

# ----------------------------------------------------------------------
#  VISUALIZACIONES
#  tiene lo necesario para graficar y animar:
#  dibujar los vectores 
#  grafica estatica 
#   
# -----------------------------------------------------------------------------


def dibujar_gradientes_grid(ax, generator, alpha, arrow_scale=0.15):
    """Dibuja todos los vectores de la cuadricula de un generator."""
    tam_grid_x = generator.TAM_GRID_X
    tam_grid_y = generator.TAM_GRID_Y
    gradients = generator.gradients

    for i in range(tam_grid_x):
        for j in range(tam_grid_y):
            x_node = i / alpha
            y_node = j / alpha
            dx, dy = gradients[i, j]
            ax.arrow(x_node, y_node, 
                     dx * arrow_scale, dy * arrow_scale, 
                     head_width=0.08 / alpha, 
                     color='blue', 
                     linewidth=1.5,
                     zorder=3)


def generar_y_graficar_estatico(x_range, y_range, alpha, generator, calculation_method_name, detail=400, title="ruido perlin estatico"):
    """Calcula el campo de ruido completo y lo muestra."""
    x_min, x_max = x_range; y_min, y_max = y_range

    # Obtenemos la función de cálculo del objeto generator
    # Usamos getattr para llamar al método del objeto por su nombre (string)
    calculation_function = getattr(generator, calculation_method_name)
    
    X = np.linspace(x_min, x_max, detail); Y = np.linspace(y_min, y_max, detail)
    campo_ruido = np.zeros((detail, detail))
    
    print(f"generando {title} en [{x_min}, {x_max}] x [{y_min}, {y_max}] (escala={alpha})...")
    
    # Bucle de barrido (llama al método del objeto)
    for i, x in enumerate(X):
        for j, y in enumerate(Y):
            campo_ruido[j, i] = calculation_function(x, y, alpha)
            
    fig, ax = plt.subplots(figsize=(8, 6))
    mapa_color = 'viridis'
    
    im = ax.imshow(campo_ruido, origin='lower', extent=[x_min, x_max, y_min, y_max], 
                    cmap=mapa_color, vmin=-1.0, vmax=1.0)
    
    dibujar_gradientes_grid(ax, generator, alpha)
    
    # Dibujar las líneas de cuadricula
    x_min_int = int(x_min); x_max_int = int(x_max)
    for i in range(x_min_int, x_max_int + 1):
        ax.axvline(i / alpha, color='red', linestyle=':', alpha=0.3)
    y_min_int = int(y_min); y_max_int = int(y_max)
    for j in range(y_min_int, y_max_int + 1):
        ax.axhline(j / alpha, color='red', linestyle=':', alpha=0.3)
        
    ax.set_title(title); ax.set_xlabel("coordenada x"); ax.set_ylabel("coordenada y")
    plt.colorbar(im, ax=ax, label="valor de salida")
    
    plt.show()


def animar_barrido_perlin(x_range, y_range, alpha, generator, calculation_method_name, detail=100, interval_ms=50):
    """
    Muestra la animación por celda.
    En el rango dado: x_range y_range
    recive tambien el generador: generator
    y lo puede hacer para cualquier funcion: calculation_method_name
    """
    x_min, x_max = x_range; y_min, y_max = y_range
    
    calculation_function = getattr(generator, calculation_method_name)

    X_coords = np.linspace(x_min, x_max, detail); Y_coords = np.linspace(y_min, y_max, detail)
    campo_ruido_animado = np.full((detail, detail), np.nan)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    im = ax.imshow(campo_ruido_animado, origin='lower', extent=[x_min, x_max, y_min, y_max], 
                    cmap='viridis', vmin=-1.0, vmax=1.0, interpolation='nearest')
    
    ax.set_title(f"animacion de ruido perlin 2d por celda (escala $\\alpha={alpha}$)")
    ax.set_xlabel("coordenada x"); ax.set_ylabel("coordenada y")
    plt.colorbar(im, ax=ax, label="valor de ruido")
    
    dibujar_gradientes_grid(ax, generator, alpha)
    
    # Dibujar cuadricula
    x_min_int = int(x_min); x_max_int = int(x_max)
    for i in range(x_min_int, x_max_int + 1):
        ax.axvline(i / alpha, color='red', linestyle=':', alpha=0.3)
    y_min_int = int(y_min); y_max_int = int(y_max)
    for j in range(y_min_int, y_max_int + 1):
        ax.axhline(j / alpha, color='red', linestyle=':', alpha=0.3)
        
    current_point, = ax.plot([], [], 'o', color='red', markersize=4, alpha=0.7, zorder=0)
    
    dist_arrow = ax.arrow(0, 0, 0, 0, 
                          width=0.01 / alpha, head_width=0.08 / alpha, 
                          color='lime', linewidth=2, zorder=2)

    frames = []
    
    # celdas a recorrer
    scaled_x_min = x_min * alpha; scaled_x_max = x_max * alpha
    scaled_y_min = y_min * alpha; scaled_y_max = y_max * alpha
    
    cell_x_indices = range(int(np.floor(scaled_x_min)), int(np.ceil(scaled_x_max)))
    cell_y_indices = range(int(np.floor(scaled_y_min)), int(np.ceil(scaled_y_max)))

    # la lista de frames (puntos a visitar) # aqui se elije el ORDEN
    for y0_cell in cell_y_indices:
        for x0_cell in cell_x_indices:
            cell_x_start = x0_cell; cell_x_end = x0_cell + 1
            cell_y_start = y0_cell; cell_y_end = y0_cell + 1
            
            i_start = np.searchsorted(X_coords, cell_x_start / alpha)
            i_end = np.searchsorted(X_coords, cell_x_end / alpha)
            j_start = np.searchsorted(Y_coords, cell_y_start / alpha)
            j_end = np.searchsorted(Y_coords, cell_y_end / alpha)
            
            for j in range(j_start, j_end):
                for i in range(i_start, i_end):
                    frames.append((i, j))

    if not frames:
        print("advertencia: no se encontraron puntos dentro de la region especificada xd")
        return

    # para cada actualizacion
    def update(frame_idx):
        i, j = frames[frame_idx]

        # el valor
        x_val = X_coords[i]; y_val = Y_coords[j]
        valor_ruido = calculation_function(x_val, y_val)
        
        # la esquina de la celda (x0, y0)
        x0 = int(np.floor(x_val * alpha)) / alpha; y0 = int(np.floor(y_val * alpha)) / alpha
        dx = x_val - x0; dy = y_val - y0
        
        # actualizamos flecha y mapa calor 
        dist_arrow.set_data(x=x0, y=y0, dx=dx, dy=dy)
        campo_ruido_animado[j, i] = valor_ruido
        im.set_data(campo_ruido_animado)
        
        current_point.set_data([x_val], [y_val])
        
        return [im, current_point, dist_arrow]

    # hacer la animacion
    ani = FuncAnimation(fig, update, frames=len(frames), blit=True, interval=interval_ms)
    
    plt.show()