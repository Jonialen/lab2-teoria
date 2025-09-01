# subset_construction.py (subset_construction.py)

from dfa import DFA

class SubsetConstruction:
    """Implementa el algoritmo de construcción de subconjuntos (AFN → AFD)"""
    
    def __init__(self):
        self.steps = []  # Para documentar el proceso
        
    def construct_dfa(self, nfa):
        """
        Convierte un AFN a AFD usando el algoritmo de construcción de subconjuntos
        Returns: (DFA, steps)
        """
        self.steps = []
        self.steps.append("=== INICIANDO CONSTRUCCIÓN DE SUBCONJUNTOS ===")
        self.steps.append(f"AFN con {len(nfa.states)} estados")
        self.steps.append(f"Alfabeto del AFN: {sorted(nfa.alphabet)}")
        
        # Inicializar AFD
        dfa = DFA()
        dfa.alphabet = nfa.alphabet.copy()  # Mismo alfabeto, sin epsilon
        
        # Paso 1: Calcular epsilon-clausura del estado inicial del AFN
        if not nfa.initial_state:
            raise ValueError("El AFN no tiene estado inicial")
        
        initial_closure = nfa.get_epsilon_closure([nfa.initial_state])
        self.steps.append(f"\nPaso 1: ε-clausura del estado inicial q{nfa.initial_state.state_id}")
        self.steps.append(f"ε-clausura({{{nfa.initial_state.state_id}}}) = {{{','.join(str(s.state_id) for s in initial_closure)}}}")
        
        # Crear estado inicial del AFD
        initial_is_final = any(s.is_final for s in initial_closure)
        initial_dfa_state = dfa.create_state(initial_closure, initial_is_final)
        dfa.set_initial_state(initial_dfa_state)
        
        self.steps.append(f"Estado inicial del AFD: {initial_dfa_state} {'(final)' if initial_is_final else ''}")
        
        # Estructuras para el algoritmo
        unprocessed_states = [initial_dfa_state]  # Cola de estados por procesar
        state_sets_created = {frozenset(s.state_id for s in initial_closure): initial_dfa_state}
        
        step_counter = 2
        
        # Paso 2: Procesar todos los estados
        while unprocessed_states:
            current_dfa_state = unprocessed_states.pop(0)
            self.steps.append(f"\nPaso {step_counter}: Procesando estado {current_dfa_state}")
            
            # Para cada símbolo del alfabeto
            for symbol in sorted(dfa.alphabet):
                self.steps.append(f"  Símbolo '{symbol}':")
                
                # Calcular el conjunto de estados alcanzables
                target_nfa_states = set()
                
                # Para cada estado del AFN en el estado actual del AFD
                for nfa_state in current_dfa_state.nfa_states:
                    transitions = nfa_state.get_transitions(symbol)
                    for target_state in transitions:
                        target_nfa_states.add(target_state)
                        self.steps.append(f"    q{nfa_state.state_id} --{symbol}--> q{target_state.state_id}")
                
                if not target_nfa_states:
                    self.steps.append(f"    No hay transiciones con '{symbol}'")
                    continue
                
                # Calcular epsilon-clausura del conjunto resultante
                epsilon_closure = nfa.get_epsilon_closure(list(target_nfa_states))
                closure_ids = sorted(s.state_id for s in epsilon_closure)
                self.steps.append(f"    ε-clausura({{{','.join(str(s.state_id) for s in target_nfa_states)}}}) = {{{','.join(map(str, closure_ids))}}}")
                
                # Verificar si ya existe un estado con este conjunto
                closure_frozenset = frozenset(s.state_id for s in epsilon_closure)
                
                if closure_frozenset in state_sets_created:
                    # Estado ya existe
                    target_dfa_state = state_sets_created[closure_frozenset]
                    self.steps.append(f"    Estado ya existe: {target_dfa_state}")
                else:
                    # Crear nuevo estado
                    is_final = any(s.is_final for s in epsilon_closure)
                    target_dfa_state = dfa.create_state(epsilon_closure, is_final)
                    state_sets_created[closure_frozenset] = target_dfa_state
                    unprocessed_states.append(target_dfa_state)
                    
                    self.steps.append(f"    Nuevo estado creado: {target_dfa_state} {'(final)' if is_final else ''}")
                
                # Añadir transición
                dfa.add_transition(current_dfa_state, symbol, target_dfa_state)
                self.steps.append(f"    Transición: {current_dfa_state} --{symbol}--> {target_dfa_state}")
            
            step_counter += 1
        
        # Resumen final
        self.steps.append(f"\n=== CONSTRUCCIÓN COMPLETADA ===")
        self.steps.append(f"AFD resultante:")
        self.steps.append(f"  Estados: {len(dfa.states)}")
        self.steps.append(f"  Estado inicial: {dfa.initial_state}")
        self.steps.append(f"  Estados finales: {[dfa.states[sid] for sid in dfa.final_states]}")
        self.steps.append(f"  Alfabeto: {sorted(dfa.alphabet)}")
        
        self.steps.append(f"\nTabla de transiciones:")
        for state_id, state in dfa.states.items():
            for symbol in sorted(dfa.alphabet):
                target = state.get_transition(symbol)
                if target:
                    self.steps.append(f"  {state} --{symbol}--> {target}")
        
        return dfa, self.steps
    
    def print_construction_steps(self, steps):
        """Imprime los pasos de la construcción"""
        for step in steps:
            print(step)
    
    def save_construction_report(self, steps, filename):
        """Guarda el reporte de construcción en un archivo"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for step in steps:
                    f.write(step + '\n')
            print(f"Reporte de construcción guardado en {filename}")
            return True
        except Exception as e:
            print(f"Error guardando reporte: {e}")
            return False


# Función de utilidad para pruebas
def test_subset_construction():
    """Función de prueba para el algoritmo de construcción de subconjuntos"""
    # Esta función será útil para probar la implementación
    from thompson import ThompsonConstructor
    from ast_builder import ASTBuilder
    from shunting_yard import ShuntingYard
    
    print("=== PRUEBA DE CONSTRUCCIÓN DE SUBCONJUNTOS ===")
    
    # Crear un AFN simple para probar
    converter = ShuntingYard()
    ast_builder = ASTBuilder()
    thompson = ThompsonConstructor()
    subset_builder = SubsetConstruction()
    
    # Expresión de prueba
    test_expr = "(a|b)*a"
    print(f"Expresión de prueba: {test_expr}")
    
    # Convertir a AFN
    postfix, _ = converter.infix_to_postfix(test_expr)
    ast_root, _ = ast_builder.build_ast(postfix)
    nfa = thompson.construct_nfa(ast_root)
    
    print(f"AFN creado con {len(nfa.states)} estados")
    
    # Convertir a AFD
    dfa, steps = subset_builder.construct_dfa(nfa)
    
    # Mostrar pasos
    subset_builder.print_construction_steps(steps)
    
    return dfa, nfa


if __name__ == "__main__":
    test_subset_construction()
