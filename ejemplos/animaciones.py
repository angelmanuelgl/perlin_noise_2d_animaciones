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
    print("--- visualizaciones animadas paso a paso ---")

    DETAIL_LEVEL = 30
    ANIMATION_INTERVAL = 1

        # ruido Perlin completo
    print("calculando el producto punto con la esquina inferior izquierda")
    animar_barrido_perlin(
        X_RANGE, 
        Y_RANGE, 
        ALPHA_SCALE, 
        generator=perlin_generator, 
        calculation_method_name='perlin_contribucion_sw', 
        detail=DETAIL_LEVEL, 
        interval_ms=ANIMATION_INTERVAL
    )
    

    # ruido Perlin completo
    print("mostrando ruido perlin completo (animado)")
    animar_barrido_perlin(
        X_RANGE, 
        Y_RANGE, 
        ALPHA_SCALE, 
        generator=perlin_generator, 
        calculation_method_name='perlin_clasico', 
        detail=DETAIL_LEVEL, 
        interval_ms=ANIMATION_INTERVAL
    )


    
    
