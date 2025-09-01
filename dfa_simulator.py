# dfa_simulator.py (dfa_simulator.py)

class DFASimulator:
    """Simula la ejecución de un AFD para verificar cadenas"""
    
    def __init__(self, dfa):
        self.dfa = dfa
        
    def simulate(self, input_string):
        """
        Simula el AFD con una cadena de entrada (Determinista)
        Retorna (accepted, steps)
        """
        steps = []
        steps.append(f"=== SIMULACIÓN DE AFD ===")
        steps.append(f"Simulando AFD con cadena: '{input_string}'")
        steps.append(f"Estado inicial: {self.dfa.initial_state}")
        
        if not self.dfa.initial_state:
            steps.append("ERROR: AFD sin estado inicial")
            return False, steps
        
        current_state = self.dfa.initial_state
        steps.append(f"Estado actual: {current_state}")
        
        # Procesar cada carácter de la cadena
        for i, symbol in enumerate(input_string):
            steps.append(f"\n--- Paso {i+1}: Procesando símbolo '{symbol}' ---")
            steps.append(f"Estado actual: {current_state}")
            
            # Buscar transición para este símbolo
            next_state = current_state.get_transition(symbol)
            
            if next_state is None:
                steps.append(f"No existe transición desde {current_state} con símbolo '{symbol}'")
                steps.append("RESULTADO: CADENA RECHAZADA - No hay transición")
                return False, steps
            
            # Ejecutar transición
            steps.append(f"Transición: {current_state} --{symbol}--> {next_state}")
            current_state = next_state
            steps.append(f"Nuevo estado actual: {current_state}")
        
        # Verificar si el estado final es de aceptación
        steps.append(f"\n--- Verificación Final ---")
        steps.append(f"Estado final alcanzado: {current_state}")
        steps.append(f"Estados finales del AFD: {[self.dfa.states[sid] for sid in self.dfa.final_states]}")
        
        is_accepted = current_state.state_id in self.dfa.final_states
        
        if is_accepted:
            steps.append("Si El estado final ES un estado de aceptación")
            steps.append("RESULTADO: CADENA ACEPTADA")
        else:
            steps.append("No El estado final NO es un estado de aceptación")
            steps.append("RESULTADO: CADENA RECHAZADA")
        
        return is_accepted, steps
    
    def simulate_multiple_strings(self, test_strings):
        """
        Simula múltiples cadenas y retorna un resumen
        Returns: [(string, accepted, brief_path), ...]
        """
        results = []
        
        print(f"\n=== SIMULACIÓN MÚLTIPLE DE AFD ===")
        print(f"Probando {len(test_strings)} cadenas...")
        
        for test_string in test_strings:
            accepted, steps = self.simulate(test_string)
            
            # Crear un path breve para el resumen
            path = [str(self.dfa.initial_state)]
            current_state = self.dfa.initial_state
            
            for symbol in test_string:
                next_state = current_state.get_transition(symbol)
                if next_state is None:
                    path.append("No")
                    break
                path.append(f"--{symbol}-->")
                path.append(str(next_state))
                current_state = next_state
            
            brief_path = " ".join(path)
            results.append((test_string, accepted, brief_path))
            
            # Mostrar resultado resumido
            result_symbol = "Si" if accepted else "No"
            print(f"  '{test_string}' -> {result_symbol}")
        
        return results
    
    def compare_with_nfa(self, nfa_simulator, test_strings):
        """
        Compara los resultados del AFD con un simulador de AFN
        Returns: (matches, comparison_results)
        """
        print(f"\n=== COMPARACIÓN AFD vs AFN ===")
        
        comparison_results = []
        matches = 0
        
        for test_string in test_strings:
            # Simular con AFD
            dfa_accepted, _ = self.simulate(test_string)
            
            # Simular con AFN
            nfa_accepted, _ = nfa_simulator.simulate(test_string)
            
            # Comparar resultados
            match = dfa_accepted == nfa_accepted
            if match:
                matches += 1
            
            comparison_results.append({
                'string': test_string,
                'dfa_result': dfa_accepted,
                'nfa_result': nfa_accepted,
                'match': match
            })
            
            # Mostrar comparación
            dfa_symbol = "Si" if dfa_accepted else "No"
            nfa_symbol = "Si" if nfa_accepted else "No"
            match_symbol = "Si" if match else "Advertencia"
            
            print(f"  '{test_string}': AFD {dfa_symbol} | AFN {nfa_symbol} | Match {match_symbol}")
        
        match_percentage = (matches / len(test_strings)) * 100
        print(f"\nCoincidencias: {matches}/{len(test_strings)} ({match_percentage:.1f}%)")
        
        return matches == len(test_strings), comparison_results
    
    def get_transition_table(self):
        """Genera la tabla de transiciones del AFD para visualización"""
        if not self.dfa.alphabet:
            return "AFD sin alfabeto definido"
        
        # Encabezado
        table = []
        header = ["Estado"] + sorted(self.dfa.alphabet) + ["Final"]
        table.append(header)
        
        # Filas para cada estado
        for state_id in sorted(self.dfa.states.keys()):
            state = self.dfa.states[state_id]
            row = [str(state)]
            
            # Transiciones para cada símbolo
            for symbol in sorted(self.dfa.alphabet):
                target = state.get_transition(symbol)
                if target:
                    row.append(str(target))
                else:
                    row.append("∅")
            
            # Marcar si es final
            row.append("Si" if state.is_final else "No")
            table.append(row)
        
        return table
    
    def print_transition_table(self):
        """Imprime la tabla de transiciones de forma legible"""
        table = self.get_transition_table()
        
        if isinstance(table, str):
            print(table)
            return
        
        print(f"\n=== TABLA DE TRANSICIONES DEL AFD ===")
        
        # Calcular anchos de columna
        col_widths = []
        for col_idx in range(len(table[0])):
            max_width = max(len(str(row[col_idx])) for row in table)
            col_widths.append(max_width + 2)
        
        # Imprimir encabezado
        header_row = table[0]
        print("+" + "+".join("-" * width for width in col_widths) + "+")
        print("|" + "|".join(f" {header_row[i]:<{col_widths[i]-1}}" for i in range(len(header_row))) + "|")
        print("+" + "+".join("-" * width for width in col_widths) + "+")
        
        # Imprimir filas de estados
        for row in table[1:]:
            print("|" + "|".join(f" {row[i]:<{col_widths[i]-1}}" for i in range(len(row))) + "|")
        
        print("+" + "+".join("-" * width for width in col_widths) + "+")


def test_dfa_simulator():
    """Función de prueba para el simulador de AFD"""
    print("=== PRUEBA DEL SIMULADOR DE AFD ===")
    
    # Importar dependencias necesarias
    from shunting_yard import ShuntingYard
    from ast_builder import ASTBuilder
    from thompson import ThompsonConstructor
    from subset_construction import SubsetConstruction
    from nfa_simulator import NFASimulator
    
    # Expresión de prueba
    test_expr = "(a|b)*a"
    print(f"Expresión de prueba: {test_expr}")
    
    # Pipeline completo: Expresión -> AFN -> AFD
    converter = ShuntingYard()
    ast_builder = ASTBuilder()
    thompson = ThompsonConstructor()
    subset_builder = SubsetConstruction()
    
    # Crear AFN
    postfix, _ = converter.infix_to_postfix(test_expr)
    ast_root, _ = ast_builder.build_ast(postfix)
    nfa = thompson.construct_nfa(ast_root)
    
    # Crear AFD
    dfa, construction_steps = subset_builder.construct_dfa(nfa)
    
    # Crear simuladores
    dfa_simulator = DFASimulator(dfa)
    nfa_simulator = NFASimulator(nfa)
    
    print(f"\nAFD creado con {len(dfa.states)} estados")
    
    # Mostrar tabla de transiciones
    dfa_simulator.print_transition_table()
    
    # Cadenas de prueba
    test_strings = ["a", "b", "aa", "ba", "aba", "bbb", "ab", ""]
    
    # Probar simulación múltiple
    results = dfa_simulator.simulate_multiple_strings(test_strings)
    
    # Comparar con AFN
    matches, comparison = dfa_simulator.compare_with_nfa(nfa_simulator, test_strings)
    
    if matches:
        print("\nSi ÉXITO: AFD y AFN producen resultados idénticos")
    else:
        print("\nAdvertencia ADVERTENCIA: AFD y AFN producen resultados diferentes")
        for comp in comparison:
            if not comp['match']:
                print(f"  Diferencia en '{comp['string']}': AFD={comp['dfa_result']}, AFN={comp['nfa_result']}")


if __name__ == "__main__":
    test_dfa_simulator()
