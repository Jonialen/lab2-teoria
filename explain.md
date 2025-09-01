# Guía de Estudio del Código: Procesador de Expresiones Regulares

Este documento es una inmersión profunda en el código fuente del proyecto. Está diseñado para ayudarte a entender cada componente, su lógica interna y cómo se conecta con el resto del sistema.

**Nota sobre la navegación**: Las referencias de código como `[ClassName.method()](#...)` son marcadores de texto. En este documento, puedes usar la función de búsqueda (Ctrl+F) con el nombre del método para encontrar rápidamente su explicación detallada.

---

## 1. Vista General y Flujo de Datos

El proyecto es un pipeline que transforma una expresión regular de texto a una máquina de estados optimizada (un AFD minimizado).

El flujo de datos es el siguiente:

`string` -> **ShuntingYard** -> `string (postfix)` -> **ASTBuilder** -> `ASTNode (árbol)` -> **ThompsonConstructor** -> `NFA` -> **SubsetConstruction** -> `DFA` -> **DFAMinimizer** -> `DFA (minimizada)`

Cada uno de estos objetos es procesado por simuladores y visualizadores.

---

## 2. Desglose Detallado del Código

### Módulo Orquestador: `main_project.py`

Este archivo es el director de orquesta. No contiene lógica de algoritmos, sino que coordina las llamadas a los demás módulos en el orden correcto.

#### `RegexProcessor.process_single_expression(expression, ...)`

Este es el método central del pipeline. Observa cómo cada paso alimenta al siguiente:

```python
# main_project.py

# PASO 1: Conversión Infix a Postfix (Shunting Yard)
postfix, shunting_steps = self.shunting_yard.infix_to_postfix(expression)

# PASO 2: Construcción de AST
ast_root, ast_steps = self.ast_builder.build_ast(postfix)

# PASO 3: Construcción de AFN (Thompson)
nfa = self.thompson.construct_nfa(ast_root)

# PASO 4: Construcción de AFD (Subconjuntos)
dfa, construction_steps = self.subset_constructor.construct_dfa(nfa)

# PASO 5: Minimización de AFD
minimized_dfa, minimization_steps = self.dfa_minimizer.minimize_dfa(dfa)

# PASO 6: Crear visualizaciones
self._create_visualizations(ast_root, nfa, dfa, minimized_dfa, expression, expr_num)

# PASO 7: Simular autómatas
simulations = self._run_simulations(nfa, dfa, minimized_dfa, test_strings)
```

---

### Módulo de Conversión: `shunting_yard.py`

Este módulo prepara la expresión regular para que pueda ser convertida en una estructura de árbol (AST).

#### `ShuntingYard.add_concatenation(tokens)`

-   **Propósito**: El principal desafío de las expresiones regulares es que la concatenación es implícita (`ab` significa `a` seguido de `b`). Este método la hace explícita insertando un carácter `.` donde corresponde.
-   **Lógica Clave**: Itera sobre los tokens y mira el token actual y el siguiente para decidir si debe insertar un `.`.

```python
# shunting_yard.py

should_concat = (
    # literal seguido de literal: ab
    (self.is_literal(curr) and self.is_literal(next_token)) or
    # literal seguido de '(': a(
    (self.is_literal(curr) and next_token == '(') or
    # ')' seguido de literal: )a
    (curr == ')' and self.is_literal(next_token)) or
    # ')' seguido de '(': )(
    (curr == ')' and next_token == '(') or
    # '*' seguido de literal: a*b
    (curr == '*' and self.is_literal(next_token)) or
    # '*' seguido de '(': a*(
    (curr == '*' and next_token == '(')
)

if should_concat:
    result.append('.')
```

#### `ShuntingYard.infix_to_postfix(infix)`

-   **Propósito**: Implementa el algoritmo Shunting Yard para reordenar la expresión de una manera que sea fácil de procesar para un constructor de árboles.
-   **Funcionamiento**:
    1.  Utiliza una **pila de operadores** y una **lista de salida**.
    2.  **Operandos** (como `a`, `b`, `ε`) van directamente a la salida.
    3.  **Operadores** (`.`, `|`) se meten en la pila. Si un operador en la pila tiene mayor o igual precedencia que el actual, se saca de la pila y se pone en la salida antes de meter el nuevo.
    4.  `(` se mete siempre en la pila.
    5.  `)` hace que se saquen todos los operadores de la pila hasta encontrar el `(`.

---

### Módulos del Árbol de Sintaxis Abstracta (AST)

#### `ast_node.py`

-   **Propósito**: Define la estructura de datos más simple: un nodo de árbol.
-   **Estructura**:
    -   `value`: El carácter del operador (`.`, `|`, `*`) o del operando (`a`, `b`).
    -   `left`, `right`: Punteros a los nodos hijos. Los operadores unarios como `*` solo usan el hijo izquierdo.
    -   `node_type`: Una etiqueta para ayudar en la visualización.

#### `ast_builder.py`

-   **Propósito**: Construir el AST a partir de la cadena postfija.
-   **`ASTBuilder.build_ast(postfix_expression)`**:
    -   **Funcionamiento**: Utiliza una pila para construir el árbol. Lee la expresión postfija de izquierda a derecha.
        -   Si el token es un **operando**, crea un nodo hoja y lo mete en la pila.
        -   Si el token es un **operador binario** (`.` o `|`), saca dos nodos de la pila (serán sus hijos derecho e izquierdo), crea un nuevo nodo padre con el operador y mete el nuevo sub-árbol en la pila.
        -   Si el token es un **operador unario** (`*`), saca un nodo de la pila (su único hijo), crea un nodo padre y mete el sub-árbol en la pila.
    -   Al final, solo debe quedar un elemento en la pila: la raíz del AST.

---

### Módulos del Autómata Finito No Determinista (AFN)

#### `nfa.py`

-   **Propósito**: Define la estructura de un AFN.
-   **`NFAState`**: Un estado que puede tener múltiples transiciones para el mismo símbolo, incluyendo `ε` (epsilon). Las transiciones se guardan en un diccionario: `{'a': [state1, state2], 'ε': [state3]}`.
-   **`NFA.get_epsilon_closure(states)`**:
    -   **Propósito**: Una de las funciones más importantes para la conversión a AFD. Calcula todos los estados a los que se puede llegar desde un conjunto de estados `states` moviéndose únicamente a través de transiciones `ε`.
    -   **Funcionamiento**: Utiliza una pila o cola para explorar los caminos `ε` de forma recursiva o iterativa hasta que no se puedan encontrar más estados.

#### `thompson.py`

-   **Propósito**: Implementa el algoritmo de Thompson, que es una forma elegante de convertir un AST en un AFN.
-   **`ThompsonConstructor._build_nfa_recursive(node)`**:
    -   **Funcionamiento**: Es un método recursivo que desciende por el AST. Cuando llega a una hoja (operando), construye un AFN base. Al volver de la recursión, combina los AFNs de sus hijos según el operador del nodo actual.
-   **Métodos de Combinación**:
    -   `_create_basic_nfa(symbol)`: Crea el AFN más simple: `(start) --symbol--> (final)`.
    -   `_concatenate_nfas(nfa1, nfa2)`: Conecta el estado final de `nfa1` con el estado inicial de `nfa2` mediante una transición `ε`.
    -   `_union_nfas(nfa1, nfa2)`: Crea un nuevo estado inicial con transiciones `ε` a los estados iniciales de `nfa1` y `nfa2`.
    -   `_kleene_star_nfa(nfa)`: Añade bucles. Crea un nuevo estado inicial y final. Añade transiciones `ε` para "saltarse" el autómata (cero veces), para entrar en él, y desde el final del autómata original de vuelta a su inicio (para la repetición).

---

### Módulos del Autómata Finito Determinista (AFD)

#### `dfa.py`

-   **Propósito**: Define la estructura de un AFD.
-   **`DFAState`**: La diferencia clave con `NFAState` es su tabla de transiciones: `{'a': state1, 'b': state2}`. Para cada símbolo, solo hay un único estado destino. No hay transiciones `ε`. Cada estado del AFD también recuerda qué conjunto de estados del AFN representa (`nfa_states`).

#### `subset_construction.py`

-   **Propósito**: Convierte un AFN en un AFD equivalente usando el algoritmo de construcción de subconjuntos.
-   **`SubsetConstruction.construct_dfa(nfa)`**:
    -   **Funcionamiento**: Es un algoritmo de exploración.
        1.  **Estado Inicial**: El estado inicial del AFD es la clausura-épsilon del estado inicial del AFN.
        2.  **Exploración**: Se utiliza una cola de estados del AFD pendientes de procesar.
        3.  **Bucle Principal**:
            a. Se saca un estado del AFD de la cola (llamémoslo `D_state`). `D_state` representa un conjunto de estados del AFN (`N_states`).
            b. Para cada símbolo del alfabeto:
                i. Se calcula a qué conjunto de estados del AFN se puede llegar desde `N_states` con ese símbolo.
                ii. Se calcula la clausura-épsilon de este nuevo conjunto.
                iii. Este resultado es un nuevo estado del AFD. Si no lo habíamos visto antes, se crea y se añade a la cola para ser procesado.
                iv. Se añade una transición en el AFD desde `D_state` al nuevo estado con el símbolo actual.
        4.  El algoritmo termina cuando la cola está vacía.

#### `dfa_minimizer.py`

-   **Propósito**: Optimiza el AFD reduciendo su número de estados al mínimo posible.
-   **`DFAMinimizer.minimize_dfa(dfa)`**:
    -   **Funcionamiento (Algoritmo de Particiones)**:
        1.  **Partición Inicial**: Se crean dos grupos (particiones) de estados: los que son finales y los que no lo son.
        2.  **Refinamiento Iterativo**: Se repite el siguiente proceso hasta que las particiones dejen de cambiar:
            a. Por cada partición actual, se comprueba si todos sus estados son "indistinguibles". Dos estados son distinguibles si para algún símbolo del alfabeto, uno transiciona a una partición y el otro a una partición diferente.
            b. Si se encuentran estados distinguibles dentro de una partición, esta se divide en sub-particiones más pequeñas.
        3.  **Construcción Final**: Cuando ya no se pueden hacer más divisiones, cada partición representa un único estado en el nuevo AFD minimizado. Se construyen las transiciones entre estos nuevos estados.

---

### Módulos de Simulación y Visualización

#### `dfa_simulator.py` y `nfa_simulator.py`

-   **Propósito**: Ejecutan una cadena de entrada en un autómata para ver si es aceptada.
-   **`DFASimulator.simulate`**: Muy sencillo. Mantiene un `current_state` y simplemente sigue la única transición posible para cada símbolo de la cadena.
-   **`NFASimulator.simulate`**: Más complejo. Mantiene un conjunto de `current_states`. Para cada símbolo, calcula el siguiente conjunto de estados posibles (incluyendo las clausuras-épsilon) y actualiza su estado.

#### Visualizadores (`..._visualizer.py`)

-   **Propósito**: Crear los diagramas `.png`.
-   **Funcionamiento**: Todos funcionan de manera similar. Recorren la estructura de datos (AST, NFA o DFA) y generan un código en lenguaje DOT, que es el lenguaje que entiende `graphviz`.
    -   Crean nodos con estilos (ej. `doublecircle` para estados finales).
    -   Crean aristas (edges) para representar las transiciones o las relaciones padre-hijo.
    -   Finalmente, usan la librería `graphviz` de Python para renderizar este código DOT en un archivo de imagen.