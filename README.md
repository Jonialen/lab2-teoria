# Laboratorio de Teoría de la Computación: Expresiones Regulares

Este proyecto contiene las implementaciones para dos laboratorios de Teoría de la Computación, enfocados en el procesamiento y visualización de expresiones regulares.

- **Laboratorio 2**: Implementa un verificador de balanceo de paréntesis y un conversor de expresiones de notación infija a postfija (usando el algoritmo Shunting Yard).
- **Laboratorio 3**: Construye y visualiza un Árbol de Sintaxis Abstracta (AST) a partir de una expresión regular en notación postfija.

## Características

### Laboratorio 2 (`main.py`)

- **Verificador de Balanceo**: Comprueba si los paréntesis `()`, corchetes `[]` y llaves `{}` en una expresión están correctamente balanceados.
- **Algoritmo Shunting Yard**: Convierte expresiones regulares de notación infija a notación postfija.
  - Maneja los operadores de unión (`|`), concatenación (`.`), y clausura de Kleene (`*`).
  - Inserta explícitamente el operador de concatenación donde es implícito.

### Laboratorio 3 (`main2.py`)

- **Constructor de AST**: Toma una expresión en notación postfija y construye su correspondiente Árbol de Sintaxis Abstracta (AST).
- **Visualizador de AST**: Genera una representación gráfica del AST utilizando `graphviz` y la guarda como una imagen PNG.
  - Distingue visualmente entre operandos, operadores unarios y operadores binarios.

## Requisitos

Para poder ejecutar ambos laboratorios, necesitas tener Python 3 instalado. Para la visualización gráfica del Laboratorio 3, se requiere una dependencia adicional.

- Python 3.x
- Graphviz

Puedes instalar la librería de Python para Graphviz usando pip:

```bash
pip install -r requirements.txt
```

**Nota:** También debes tener instalado el software de Graphviz en tu sistema operativo. Puedes encontrar las instrucciones de instalación en el [sitio web oficial de Graphviz](https://graphviz.org/download/).

## Uso

Las expresiones a procesar deben ser colocadas en el archivo `expressions.txt`, una por línea.

### Ejecutar Laboratorio 2

Este script verificará el balanceo de las expresiones y las convertirá a notación postfija.

```bash
python main.py
```

Los resultados se mostrarán en la consola y se guardará un resumen en `output.txt`.

### Ejecutar Laboratorio 3

Este script convertirá las expresiones a postfija, construirá los ASTs y generará una imagen (`.png`) para cada uno.

```bash
python main2.py
```

Las imágenes de los árboles (`ast_expr_1.png`, `ast_expr_2.png`, etc.) se guardarán en el directorio principal del proyecto.

## Estructura del Proyecto

```
.
├── main.py                 # Punto de entrada para Lab 2
├── main2.py                # Punto de entrada para Lab 3
├── shunting_yard.py        # Implementación del algoritmo Shunting Yard
├── expression_balancer.py  # Lógica para verificar el balanceo de paréntesis
├── ast_builder.py          # Lógica para construir el AST
├── ast_node.py             # Define la estructura de un nodo del AST
├── ast_visualizer.py       # Lógica para visualizar el AST con Graphviz
├── expressions.txt         # Archivo de entrada con las expresiones a procesar
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```