# dfa_minimizer.py (dfa_minimizer.py)

class DFAMinimizer:
    """Implementa el algoritmo de minimización de AFD usando particiones"""
    
    def __init__(self):
        self.steps = []  # Para documentar el proceso
        
    def minimize_dfa(self, dfa):
        """
        Minimiza un AFD usando el algoritmo de particiones
        Returns: (minimized_dfa, steps)
        """
        self.steps = []
        self.steps.append("=== INICIANDO MINIMIZACIÓN DE AFD ===")
        self.steps.append(f"AFD original con {len(dfa.states)} estados")
        
        # Paso 1: Eliminar estados no alcanzables
        cleaned_dfa = self._remove_unreachable_states(dfa)
        
        if len(cleaned_dfa.states) == 0:
            self.steps.append("ERROR: No quedan estados después de limpiar")
            return cleaned_dfa, self.steps
        
        # Paso 2: Crear particiones iniciales
        partitions = self._create_initial_partitions(cleaned_dfa)
        
        # Paso 3: Refinar particiones iterativamente
        final_partitions = self._refine_partitions(cleaned_dfa, partitions)
        
        # Paso 4: Construir AFD minimizado
        minimized_dfa = self._construct_minimized_dfa(cleaned_dfa, final_partitions)
        
        self.steps.append(f"\n=== MINIMIZACIÓN COMPLETADA ===")
        self.steps.append(f"Estados originales: {len(dfa.states)}")
        self.steps.append(f"Estados después de limpieza: {len(cleaned_dfa.states)}")
        self.steps.append(f"Estados minimizados: {len(minimized_dfa.states)}")
        self.steps.append(f"Reducción total: {len(dfa.states) - len(minimized_dfa.states)} estados")
        
        return minimized_dfa, self.steps
    
    def _remove_unreachable_states(self, dfa):
        """Elimina estados no alcanzables desde el estado inicial"""
        from dfa import DFA  # Import local para evitar dependencias circulares
        
        self.steps.append(f"\nPaso 1: Eliminando estados no alcanzables")
        
        if not dfa.initial_state:
            self.steps.append("No hay estado inicial definido")
            return dfa
        
        # Encontrar estados alcanzables usando BFS
        reachable_states = set()
        queue = [dfa.initial_state]
        reachable_states.add(dfa.initial_state.state_id)
        
        while queue:
            current_state = queue.pop(0)
            for symbol, target_state in current_state.transitions.items():
                if target_state.state_id not in reachable_states:
                    reachable_states.add(target_state.state_id)
                    queue.append(target_state)
        
        unreachable_states = set(dfa.states.keys()) - reachable_states
        
        self.steps.append(f"Estados alcanzables: {sorted(reachable_states)}")
        if unreachable_states:
            self.steps.append(f"Estados no alcanzables eliminados: {sorted(unreachable_states)}")
        else:
            self.steps.append("Todos los estados son alcanzables")
        
        # Crear nuevo AFD sin estados no alcanzables
        if len(unreachable_states) == 0:
            return dfa  # No hay nada que limpiar
        
        cleaned_dfa = DFA()
        cleaned_dfa.alphabet = dfa.alphabet.copy()
        
        # Mapeo de estados viejos a nuevos
        state_mapping = {}
        
        # Crear estados alcanzables
        for old_state_id in reachable_states:
            old_state = dfa.states[old_state_id]
            new_state = cleaned_dfa.create_state(old_state.nfa_states, old_state.is_final)
            state_mapping[old_state_id] = new_state
            
            # Establecer estado inicial
            if old_state_id == dfa.initial_state.state_id:
                cleaned_dfa.set_initial_state(new_state)
        
        # Recrear transiciones
        for old_state_id in reachable_states:
            old_state = dfa.states[old_state_id]
            new_from_state = state_mapping[old_state_id]
            
            for symbol, old_target_state in old_state.transitions.items():
                if old_target_state.state_id in reachable_states:
                    new_target_state = state_mapping[old_target_state.state_id]
                    cleaned_dfa.add_transition(new_from_state, symbol, new_target_state)
        
        return cleaned_dfa
    
    def _create_initial_partitions(self, dfa):
        """Crea las particiones iniciales: estados finales vs no finales"""
        self.steps.append(f"\nPaso 2: Creando particiones iniciales")
        
        final_states = []
        non_final_states = []
        
        for state_id, state in dfa.states.items():
            if state.is_final:
                final_states.append(state_id)
            else:
                non_final_states.append(state_id)
        
        partitions = []
        if non_final_states:
            partitions.append(sorted(non_final_states))
            self.steps.append(f"Partición 0 (no finales): {sorted(non_final_states)}")
        
        if final_states:
            partitions.append(sorted(final_states))
            self.steps.append(f"Partición {len(partitions)-1} (finales): {sorted(final_states)}")
        
        self.steps.append(f"Total de particiones iniciales: {len(partitions)}")
        return partitions
    
    def _refine_partitions(self, dfa, initial_partitions):
        """Refina las particiones iterativamente hasta que no cambien"""
        self.steps.append(f"\nPaso 3: Refinando particiones")
        
        partitions = [partition[:] for partition in initial_partitions]  # Copia profunda
        iteration = 0
        
        while True:
            iteration += 1
            self.steps.append(f"\n--- Iteración {iteration} ---")
            self.steps.append(f"Particiones actuales: {partitions}")
            
            new_partitions = []
            partition_changed = False
            
            for partition_idx, partition in enumerate(partitions):
                self.steps.append(f"\nProcesando partición {partition_idx}: {partition}")
                
                # Si la partición tiene solo un estado, no se puede refinar
                if len(partition) <= 1:
                    new_partitions.append(partition)
                    self.steps.append(f"  Partición con ≤1 estado, no se refina")
                    continue
                
                # Refinar esta partición
                refined_partitions = self._refine_single_partition(dfa, partition, partitions)
                
                if len(refined_partitions) > 1:
                    partition_changed = True
                    self.steps.append(f"  Partición refinada en {len(refined_partitions)} subparticiones:")
                    for i, sub_partition in enumerate(refined_partitions):
                        self.steps.append(f"    Subpartición {i}: {sub_partition}")
                else:
                    self.steps.append(f"  Partición no requiere refinamiento")
                
                new_partitions.extend(refined_partitions)
            
            partitions = new_partitions
            
            if not partition_changed:
                self.steps.append(f"\nNo hay cambios en iteración {iteration}, terminando refinamiento")
                break
            
            if iteration > 10:  # Protección contra bucles infinitos
                self.steps.append(f"\nLímite de iteraciones alcanzado ({iteration})")
                break
        
        self.steps.append(f"\nParticiones finales: {partitions}")
        return partitions
    
    def _refine_single_partition(self, dfa, partition, all_partitions):
        """Refina una sola partición basándose en el comportamiento con cada símbolo"""
        # Agrupar estados por su comportamiento de transición
        behavior_groups = {}
        
        for state_id in partition:
            state = dfa.states[state_id]
            
            # Crear "firma" del comportamiento de este estado
            behavior = []
            for symbol in sorted(dfa.alphabet):
                target_state = state.get_transition(symbol)
                if target_state:
                    target_partition = self._find_partition_containing(target_state.state_id, all_partitions)
                    behavior.append(target_partition)
                else:
                    behavior.append(-1)  # Sin transición
            
            behavior_tuple = tuple(behavior)
            
            if behavior_tuple not in behavior_groups:
                behavior_groups[behavior_tuple] = []
            behavior_groups[behavior_tuple].append(state_id)
        
        # Convertir grupos a lista de particiones
        refined_partitions = [sorted(group) for group in behavior_groups.values()]
        return refined_partitions
    
    def _find_partition_containing(self, state_id, partitions):
        """Encuentra el índice de la partición que contiene el estado dado"""
        for partition_idx, partition in enumerate(partitions):
            if state_id in partition:
                return partition_idx
        return -1  # No encontrado
    
    def _construct_minimized_dfa(self, original_dfa, final_partitions):
        """Construye el AFD minimizado a partir de las particiones finales"""
        from dfa import DFA  # Import local
        
        self.steps.append(f"\nPaso 4: Construyendo AFD minimizado")
        
        minimized_dfa = DFA()
        minimized_dfa.alphabet = original_dfa.alphabet.copy()
        
        # Crear mapeo de particiones a estados nuevos
        partition_to_state = {}
        state_to_partition = {}  # Para encontrar rápidamente la partición de un estado
        
        # Crear estados para cada partición
        for partition_idx, partition in enumerate(final_partitions):
            # Determinar si esta partición representa un estado final
            representative_state_id = partition[0]  # Usar el primer estado como representativo
            representative_state = original_dfa.states[representative_state_id]
            
            # Todos los estados en una partición deben tener la misma finalidad
            is_final = representative_state.is_final
            
            # Obtener conjunto de estados del AFN (unión de todos los estados de la partición)
            nfa_states_union = set()
            for state_id in partition:
                state = original_dfa.states[state_id]
                nfa_states_union.update(state.nfa_states)
            
            new_state = minimized_dfa.create_state(nfa_states_union, is_final)
            partition_to_state[partition_idx] = new_state
            
            # Mapear todos los estados de esta partición al nuevo estado
            for state_id in partition:
                state_to_partition[state_id] = partition_idx
            
            self.steps.append(f"Estado {new_state.state_id} representa partición {partition_idx}: {partition}")
        
        # Establecer estado inicial
        if original_dfa.initial_state:
            initial_partition_idx = state_to_partition[original_dfa.initial_state.state_id]
            initial_new_state = partition_to_state[initial_partition_idx]
            minimized_dfa.set_initial_state(initial_new_state)
            self.steps.append(f"Estado inicial: {initial_new_state.state_id}")
        
        # Crear transiciones
        for partition_idx, partition in enumerate(final_partitions):
            from_state = partition_to_state[partition_idx]
            representative_old_state = original_dfa.states[partition[0]]
            
            for symbol in minimized_dfa.alphabet:
                target_old_state = representative_old_state.get_transition(symbol)
                if target_old_state:
                    target_partition_idx = state_to_partition[target_old_state.state_id]
                    target_new_state = partition_to_state[target_partition_idx]
                    minimized_dfa.add_transition(from_state, symbol, target_new_state)
                    
                    self.steps.append(f"Transición: {from_state.state_id} --{symbol}--> {target_new_state.state_id}")
        
        return minimized_dfa
    
    def get_minimization_report(self, original_dfa, minimized_dfa, steps):
        """Genera un reporte detallado de la minimización"""
        report = []
        report.append("=" * 60)
        report.append("REPORTE DE MINIMIZACIÓN DE AFD")
        report.append("=" * 60)
        
        # Estadísticas
        report.append(f"Estados originales: {len(original_dfa.states)}")
        report.append(f"Estados minimizados: {len(minimized_dfa.states)}")
        reduction = len(original_dfa.states) - len(minimized_dfa.states)
        percentage = (reduction / len(original_dfa.states)) * 100 if len(original_dfa.states) > 0 else 0
        report.append(f"Reducción: {reduction} estados ({percentage:.1f}%)")
        report.append(f"Alfabeto: {sorted(original_dfa.alphabet)}")
        
        # Estados finales
        orig_final = [f"q{sid}" for sid in original_dfa.final_states]
        min_final = [f"q{sid}" for sid in minimized_dfa.final_states]
        report.append(f"Estados finales originales: {orig_final}")
        report.append(f"Estados finales minimizados: {min_final}")
        
        report.append("\n" + "=" * 60)
        report.append("PASOS DETALLADOS")
        report.append("=" * 60)
        
        for step in steps:
            report.append(step)
        
        return report
    
    def save_minimization_report(self, report, filename):
        """Guarda el reporte de minimización en un archivo"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for line in report:
                    f.write(line + '\n')
            print(f"Reporte de minimización guardado en {filename}")
            return True
        except Exception as e:
            print(f"Error guardando reporte: {e}")
            return False


def test_dfa_minimizer():
    """Función de prueba para el minimizador de AFD"""
    print("=== PRUEBA DEL MINIMIZADOR DE AFD ===")
    
    # Importar dependencias
    from shunting_yard import ShuntingYard
    from ast_builder import ASTBuilder
    from thompson import ThompsonConstructor
    from subset_construction import SubsetConstruction
    from dfa_simulator import DFASimulator
    
    # Expresión de prueba que debería generar estados redundantes
    test_expr = "(a|b)*a(a|b)"
    print(f"Expresión de prueba: {test_expr}")
    
    # Pipeline completo
    converter = ShuntingYard()
    ast_builder = ASTBuilder()
    thompson = ThompsonConstructor()
    subset_builder = SubsetConstruction()
    minimizer = DFAMinimizer()
    
    # Crear AFN
    postfix, _ = converter.infix_to_postfix(test_expr)
    ast_root, _ = ast_builder.build_ast(postfix)
    nfa = thompson.construct_nfa(ast_root)
    print(f"AFN creado con {len(nfa.states)} estados")
    
    # Crear AFD
    dfa, construction_steps = subset_builder.construct_dfa(nfa)
    print(f"AFD creado con {len(dfa.states)} estados")
    
    # Minimizar AFD
    minimized_dfa, minimization_steps = minimizer.minimize_dfa(dfa)
    print(f"AFD minimizado con {len(minimized_dfa.states)} estados")
    
    # Mostrar pasos de minimización
    print(f"\n=== PASOS DE MINIMIZACIÓN ===")
    for step in minimization_steps:
        print(step)
    
    # Generar reporte
    report = minimizer.get_minimization_report(dfa, minimized_dfa, minimization_steps)
    minimizer.save_minimization_report(report, "minimization_report.txt")
    
    # Probar que los AFDs son equivalentes
    print(f"\n=== VERIFICACIÓN DE EQUIVALENCIA ===")
    test_strings = ["a", "aa", "aaa", "ab", "ba", "aba", "bab", ""]
    
    original_simulator = DFASimulator(dfa)
    minimized_simulator = DFASimulator(minimized_dfa)
    
    all_match = True
    for test_string in test_strings:
        orig_result, _ = original_simulator.simulate(test_string)
        min_result, _ = minimized_simulator.simulate(test_string)
        
        match = orig_result == min_result
        if not match:
            all_match = False
        
        orig_symbol = "Si" if orig_result else "No"
        min_symbol = "Si" if min_result else "No"
        match_symbol = "Si" if match else "Advertencia"
        
        print(f"  '{test_string}': Original {orig_symbol} | Minimizado {min_symbol} | Match {match_symbol}")
    
    if all_match:
        print(f"\nSi ÉXITO: AFD original y minimizado son equivalentes")
    else:
        print(f"\nAdvertencia ERROR: AFDs no son equivalentes")
    
    return minimized_dfa, dfa


if __name__ == "__main__":
    test_dfa_minimizer()
