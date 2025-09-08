# Proyecto de Algoritmos de Búsqueda en Grafos

Este proyecto implementa y compara diversos algoritmos de búsqueda en grafos, considerando grafos estáticos y dinámicos, métricas personalizadas y visualizaciones interactivas. El enfoque se centra en escenarios del sector (por ejemplo, transporte, energía o salud) para optimizar rutas o procesos.

Realizado por:
- Diego Alejandro Guevara
- Paula Alejandra Ortiz
- Mariana Ruge Vargas


---

## Contenido del proyecto

1. **Comparación empírica de algoritmos sin heurística**
   - Implementación de **DFS**, **BFS** y **UCS** para encontrar caminos entre dos nodos críticos del grafo.
   - Generación de tablas comparativas que incluyen:
     - Número de nodos explorados.
     - Costo del camino encontrado.
     - Tiempo de ejecución.
   - Permite analizar la eficiencia de cada algoritmo según la topología del grafo.

2. **Problema con grafo dinámico**
   - Modificación dinámica de los costos de las aristas (ej. congestión, disponibilidad de rutas).
   - Ejecución de **A*** antes y después del cambio.
   - Análisis de sensibilidad de A* frente a cambios de costos y efectos de la heurística (subestimación/sobreestimación).
   - Explicación de por qué **UCS siempre encuentra la solución óptima** si los costos son positivos.
   - Simulación de incremento del tamaño del grafo y análisis del impacto en nodos explorados y tiempo de ejecución.

3. **Buscador Inteligente**
   - Interfaz en consola donde el usuario puede:
     - Seleccionar algoritmo: BFS, DFS, UCS, GBFS, A*, A* con pesos personalizados.
     - Ingresar nodo inicial y objetivo.
   - Salida:
     - Camino encontrado.
     - Costo (si aplica).
     - Número de nodos explorados.
   - Permite comparar resultados y recomendar algoritmos según el tipo de grafo.

4. **Escenario real con pesos dinámicos**
   - Cada nodo y arista del grafo tiene atributos reales del sector (costo, tiempo, distancia, contaminación, etc.).
   - El usuario puede seleccionar la métrica de optimización.
   - Si los pesos cambian, la heurística se adapta automáticamente.
   - Visualización interactiva del grafo:
     - Algoritmos sin heurística (BFS, DFS).
     - Algoritmos con heurística (A*).
     - Animación que muestra cómo los algoritmos exploran los nodos.

5. **Heurística personalizada**
   - Función heurística adaptada al dominio del proyecto (logística, tráfico, robots, etc.).
   - Explicación de la lógica y admisibilidad de la heurística.
   - Comparación de rendimiento frente a BFS y A* con heurística estándar.
   - Análisis de limitaciones y condiciones que podrían afectar la búsqueda óptima.

---

## Estructura de archivos

- Parcial 1 IA:  Punto 1 y 2
[Link al colab](https://colab.research.google.com/drive/1fBJsq2tXcKT9RhbKYgcu2XuJJHDw_I6M?usp=sharing "Link al colab")
- Parcial 1 Parte 2: Punto 4
[Link al colab](https://colab.research.google.com/drive/1fBJsq2tXcKT9RhbKYgcu2XuJJHDw_I6M?usp=sharing "Link al colab")

- Parcial 1 - Punto 5
[Link al colab](https://colab.research.google.com/drive/1Ow_iUl4h2VDbk7I2eGXGmUZkpVLesB08?usp=sharing "Link al colab")

- Rutas.py : Grafo interactivo

---

## Requisitos

- Python 3.9+
- Librerías:
  - `networkx`
  - `matplotlib`
  - `pyvis`
  - `heapq`
  - `time`
  - `webbrowser`
  - `collections`

    	python -m venv venv

Instalación rápida con pip:
	 pip install -r requirements.txt

# Windows
	venv\Scripts\activate
# macOS / Linux
	source venv/bin/activate

Instalar dependencias:

```
	pip install -r requirements.txt

```
**Ejecutar el código principal:**

```
	python rutas.py
```

**Instrucciones dentro de la consola:**

1. Seleccionar métrica de optimización (latencia, costo, ancho_banda, riesgo_pirateria).

3. Ingresar nodo inicial y nodo objetivo.

5. Ver resultados:

7. Caminos encontrados por BFS, DFS, UCS o A*.

9. Costo y número de nodos explorados.
