# Visualizaciones y Animaciones del Ruido de Perlin en Python

Este repositorio contiene una implementación modular del Ruido de Perlin 2D:
- visualizaciones estáticas 
- visualizaciones animadas que muestran paso a paso cómo se calcula el aporte de cada esquina, la interpolación y el valor final.

Mi objetivo principal fue explicar de forma visual y didáctica cómo funciona el algoritmo, mediante animaciones que muestran:
- El vector gradiente de cada esquina  
- El producto punto con cada esquina  
- La aplicación de la función de suavizado (*fade*)  
- Aportes individuales de las esquinas
- Ruido Perlin completo



##  Estructura del repositorio
```
│   .gitignore
│   README.md
│
├───ejemplos
│       animaciones.py           # Script para generar animaciones y demostraciones
│       estatico.py              # Script para visualizaciones estáticas
│
└───src
        perlin_base.py           # Funciones fundamentales (gradientes, fade, interpolación)
        perlin_modificaciones.py # Contiene PerlinNoiseGenerator y variantes
        perlin_visualizaciones.py# Funciones que generan gráficas y animaciones
        __init__.py              # Indica que src es un paquete
```


## Ejecutar los ejemplos

### Instala dependencias:

```bash
pip install numpy matplotlib sys 
````

---

### Ejecuta animaciones desde la carpeta `ejemplos/`


```bash
python ejemplos/animaciones.py
```

Generara ventanas de Matplotlib que muestran de manera animada:
* Contribuciones individuales del ruido
* Visualización del ruido Perlin completo
---



```bash
python ejemplos/estatico.py
```

Generara ventanas de Matplotlib que muestran los siguientes paso
* Contribucion del producto punto de una esquina
* promedio de los 4 productos punto (sin interpolacion)
* Ruido Perlin con interpolacion lineal (sin suavizado)
* Ruido Perlin (resultado final)

---


## Parametros y cambios

El script `animaciones.py` permite ejecutar animaciones cambiando parámetros como:

```python
perlin_generator = PerlinNoiseGenerator(
    tam_grid_x=5, 
    tam_grid_y=4, 
    seed=42
)

animar_barrido_perlin(
    (0.0, 4.0), 
    (0.0, 3.0),
    1.0,
    generator=perlin_generator,
    calculation_method_name='perlin_clasico',
    detail=30,
    interval_ms=1
)
```

Esto produce un barrido 2D donde el valor del ruido se va mostrando cuadro por cuadro.

---

## Archivos principales

### `src/perlin_base.py`

* Gradientes
* Fade
* Producto punto
* Interpolación lineal 

### `src/perlin_modificaciones.py`

* Clase PerlinNoiseGenerator
* Métodos específicos:

  * perlin_clasico
  * perlin_contribucion_sw
  * perlin_linear
  * perlin_promedio

### `src/perlin_visualizaciones.py`

* Gráficas estáticas
* Animaciones de Barridos en cada casilla 
* Funciones auxiliares de visualización



## Proximas cosas y mejoras ( .. en construccion)

* Convertir el proyecto en un **paquete instalable** (`pip install perlin-visuals`)
* Eliminar la necesidad de manipular `sys.path`

---

## Autor

Ángel Manuel Gonzalez Lopez
Estudiante de Computación Matemática


