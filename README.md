# Laboratorio de Teoría de la Computación: Expresiones Regulares

Este proyecto implementa un pipeline completo para el procesamiento, simulación y visualización de expresiones regulares, incluyendo:

- Conversión infijo → postfijo (Shunting Yard)
- Construcción de Árbol de Sintaxis Abstracta (AST)
- Construcción de AFN (Thompson)
- Construcción de AFD (Subconjuntos)
- Minimización de AFD
- Simulación de cadenas en AFN y AFD
- Visualización de AST, AFN y AFD con Graphviz

## Estructura del Proyecto

```
.
├── main.py                 # Balanceo y conversión infijo→postfijo (Lab 2)
├── main2.py                # Construcción y visualización de AST (Lab 3)
├── main3.py                # Pipeline hasta AFN y simulación (Lab 4)
├── main_project.py         # Pipeline completo: AST, AFN, AFD, minimización, simulación, visualización
├── shunting_yard.py        # Algoritmo Shunting Yard
├── expression_balancer.py  # Verificador de balanceo de paréntesis
├── ast_builder.py          # Construcción de AST desde postfijo
├── ast_node.py             # Nodo del AST
├── ast_visualizer.py       # Visualización de AST con Graphviz
├── thompson.py             # Construcción de AFN (Thompson)
├── nfa.py                  # Estructura y operaciones de AFN
├── nfa_visualizer.py       # Visualización de AFN
├── nfa_simulator.py        # Simulación de AFN
├── subset_construction.py  # Construcción de AFD (subconjuntos)
├── dfa.py                  # Estructura y operaciones de AFD
├── dfa_visualizer.py       # Visualización de AFD
├── dfa_simulator.py        # Simulación de AFD
├── dfa_minimizer.py        # Minimización de AFD
├── expressions.txt         # Expresiones regulares de entrada
├── requirements.txt        # Dependencias Python
├── output/                 # Archivos generados (visualizaciones, reportes)
└── README.md               # Este archivo
```

## Requisitos

- Python 3.x
- [Graphviz](https://graphviz.org/download/) (software y librería Python)

Instala la dependencia de Python con:

```sh
pip install -r requirements.txt
```

**Nota:** Debes instalar también el software de Graphviz en tu sistema operativo para generar imágenes.

## Uso

Coloca tus expresiones regulares (una por línea) en `expressions.txt`.

### Ejecución rápida del pipeline completo

```sh
python main_project.py
```

Esto generará:

- Visualizaciones PNG de AST, AFN, AFD y AFD minimizado en `output/`
- Un reporte resumen en `output/resumen_procesamiento.txt`
- Simulación de cadenas de prueba en cada autómata

### Ejecución por etapas

- **Balanceo y conversión a postfijo:**

  ```sh
  python main.py
  ```

  Resultados en consola y en `output.txt`.

- **Construcción y visualización de AST:**

  ```sh
  python main2.py
  ```

  Imágenes `ast_expr_X.png` en el directorio principal.

- **Pipeline hasta AFN y simulación:**
  ```sh
  python main3.py
  ```
  Imágenes `ast_expr_X.png`, `nfa_expr_X.png` y simulaciones en consola.

## Visualizaciones

Las imágenes generadas muestran:

- **AST:** Estructura sintáctica de la expresión.
- **AFN:** Autómata de Thompson.
- **AFD:** Autómata determinista (construcción de subconjuntos).
- **AFD Min:** Autómata determinista minimizado.

## Reportes

- `output/resumen_procesamiento.txt`: Estadísticas y resultados de cada expresión.
- `minimization_report.txt`: Detalles del proceso de minimización de AFD.

## Créditos

Desarrollado para el curso de Teoría de la Computación, Universidad del Valle de Guatemala.

---
