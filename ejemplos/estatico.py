import sys
from pathlib import Path

# directorio raiz del proyecto al PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

# ahora si los imports ya funcionan
from src.perlin_modificaciones import PerlinNoiseGenerator 
from src.perlin_visualizaciones import animar_barrido_perlin, generar_y_graficar_estatico

if __name__ == "__main__":
    
    # --- configuracipn ---
    X_RANGE = (0.0, 4.0)
    Y_RANGE = (0.0, 3.0)
    ALPHA_SCALE = 1.0
    GRID_X = 5
    GRID_Y = 4
    SEED = 42
    
    # --- instancia del generador ---
    perlin_generator = PerlinNoiseGenerator(
        tam_grid_x=GRID_X, 
        tam_grid_y=GRID_Y, 
        seed=SEED
    )
    
    # --- --- --- --- --- --- --- --- ---
    print("--- visualizaciones estaticas ---")
    
    # --- contribucion del producto punto sw ---
    generar_y_graficar_estatico(
        X_RANGE, Y_RANGE, ALPHA_SCALE, 
        generator=perlin_generator,
        calculation_method_name='perlin_contribucion_sw',
        title="contribucion del producto punto esquina sw"
    )

    # --- promedio simple de productos punto
    generar_y_graficar_estatico(
        X_RANGE, Y_RANGE, ALPHA_SCALE, 
        generator=perlin_generator,
        calculation_method_name='perlin_promedio',
        title="promedio de los 4 productos punto (sin interpolacion)"
    )

    # --- ruido perlin sin suavizado (lineal)
    generar_y_graficar_estatico(
        X_RANGE, Y_RANGE, ALPHA_SCALE, 
        generator=perlin_generator,
        calculation_method_name='perlin_linear',
        title="Ruido Perlin con interpolacion lineal (sin suavizado)"
    )

    # --- ruido perlin completo
    generar_y_graficar_estatico(
        X_RANGE, Y_RANGE, ALPHA_SCALE, 
        generator=perlin_generator,
        calculation_method_name='perlin_clasico',
        title="Ruido Perlin (resultado final)"
    )

