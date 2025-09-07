# thompson.py (thompson.py)

from nfa import NFA


class ThompsonConstructor:
    """Implementa el algoritmo de Thompson para construir AFN desde AST"""
    
    def __init__(self):
        pass
    
    def construct_nfa(self, ast_root):
        """Construye un AFN a partir del AST usando el algoritmo de Thompson"""
        if ast_root is None:
            # AFN vacío
            nfa = NFA()
            initial = nfa.create_state()
            final = nfa.create_state(is_final=True)
            nfa.set_initial_state(initial)
            nfa.add_transition(initial, 'ε', final)
            return nfa
        
        return self._build_nfa_recursive(ast_root)
    
    def _build_nfa_recursive(self, node):
        """Construye recursivamente el AFN para un nodo del AST"""

        if node.node_type == 'operand' or node.node_type == 'escaped_operand':
            return self._create_basic_nfa(node.value)
        elif node.value == '.':  # Concatenación
            return self._concatenate_nfas(
                self._build_nfa_recursive(node.left),
                self._build_nfa_recursive(node.right)
            )
        elif node.value == '|':  # Unión
            return self._union_nfas(
                self._build_nfa_recursive(node.left),
                self._build_nfa_recursive(node.right)
            )
        elif node.value == '*':  # Estrella de Kleene
            return self._kleene_star_nfa(
                self._build_nfa_recursive(node.left)
            )
        else:
            raise ValueError(f"Operador no soportado: {node.value}")
    
    def _create_basic_nfa(self, symbol):
        """Crea un AFN básico para un símbolo individual"""
        nfa = NFA()
        initial = nfa.create_state()
        final = nfa.create_state(is_final=True)
        
        nfa.set_initial_state(initial)
        
        if symbol == 'ε':
            nfa.add_transition(initial, 'ε', final)
        else:
            nfa.add_transition(initial, symbol, final)
        
        return nfa
    
    def _concatenate_nfas(self, nfa1, nfa2):
        """Concatena dos AFNs usando transiciones épsilon"""
        # Crear un nuevo AFN que combine ambos
        result_nfa = NFA()
        
        # Copiar estados de nfa1
        state_mapping1 = {}
        for state_id, state in nfa1.states.items():
            new_state = result_nfa.create_state(is_final=False)
            state_mapping1[state_id] = new_state
        
        # Copiar estados de nfa2
        state_mapping2 = {}
        for state_id, state in nfa2.states.items():
            new_state = result_nfa.create_state(is_final=state.is_final)
            state_mapping2[state_id] = new_state
        
        # Copiar transiciones de nfa1
        for state_id, state in nfa1.states.items():
            for symbol, targets in state.transitions.items():
                for target in targets:
                    result_nfa.add_transition(
                        state_mapping1[state_id],
                        symbol,
                        state_mapping1[target.state_id]
                    )
        
        # Copiar transiciones de nfa2
        for state_id, state in nfa2.states.items():
            for symbol, targets in state.transitions.items():
                for target in targets:
                    result_nfa.add_transition(
                        state_mapping2[state_id],
                        symbol,
                        state_mapping2[target.state_id]
                    )
        
        # Establecer estado inicial
        result_nfa.set_initial_state(state_mapping1[nfa1.initial_state.state_id])
        
        # Conectar estados finales de nfa1 con el inicial de nfa2
        for final_state_id in nfa1.final_states:
            # Remover la marca de final del estado de nfa1
            state_mapping1[final_state_id].is_final = False
            if final_state_id in result_nfa.final_states:
                result_nfa.final_states.remove(final_state_id)
            
            # Añadir transición épsilon
            result_nfa.add_transition(
                state_mapping1[final_state_id],
                'ε',
                state_mapping2[nfa2.initial_state.state_id]
            )
        
        return result_nfa
    
    def _union_nfas(self, nfa1, nfa2):
        """Une dos AFNs creando un nuevo estado inicial"""
        result_nfa = NFA()
        
        # Crear nuevo estado inicial
        new_initial = result_nfa.create_state()
        result_nfa.set_initial_state(new_initial)
        
        # Copiar estados de ambos AFNs
        state_mapping1 = {}
        for state_id, state in nfa1.states.items():
            new_state = result_nfa.create_state(is_final=state.is_final)
            state_mapping1[state_id] = new_state
        
        state_mapping2 = {}
        for state_id, state in nfa2.states.items():
            new_state = result_nfa.create_state(is_final=state.is_final)
            state_mapping2[state_id] = new_state
        
        # Copiar transiciones
        for state_id, state in nfa1.states.items():
            for symbol, targets in state.transitions.items():
                for target in targets:
                    result_nfa.add_transition(
                        state_mapping1[state_id],
                        symbol,
                        state_mapping1[target.state_id]
                    )
        
        for state_id, state in nfa2.states.items():
            for symbol, targets in state.transitions.items():
                for target in targets:
                    result_nfa.add_transition(
                        state_mapping2[state_id],
                        symbol,
                        state_mapping2[target.state_id]
                    )
        
        # Conectar el nuevo inicial con los iniciales de ambos AFNs
        result_nfa.add_transition(
            new_initial, 'ε', state_mapping1[nfa1.initial_state.state_id]
        )
        result_nfa.add_transition(
            new_initial, 'ε', state_mapping2[nfa2.initial_state.state_id]
        )
        
        return result_nfa
    
    def _kleene_star_nfa(self, nfa):
        """Aplica la estrella de Kleene a un AFN"""
        result_nfa = NFA()
        
        # Crear nuevo estado inicial y final
        new_initial = result_nfa.create_state()
        new_final = result_nfa.create_state(is_final=True)
        result_nfa.set_initial_state(new_initial)
        
        # Copiar estados del AFN original
        state_mapping = {}
        for state_id, state in nfa.states.items():
            new_state = result_nfa.create_state(is_final=False)
            state_mapping[state_id] = new_state
        
        # Copiar transiciones
        for state_id, state in nfa.states.items():
            for symbol, targets in state.transitions.items():
                for target in targets:
                    result_nfa.add_transition(
                        state_mapping[state_id],
                        symbol,
                        state_mapping[target.state_id]
                    )
        
        # Transiciones para la estrella de Kleene
        # 1. Nuevo inicial -> nuevo final (cadena vacía)
        result_nfa.add_transition(new_initial, 'ε', new_final)
        
        # 2. Nuevo inicial -> inicial original
        result_nfa.add_transition(
            new_initial, 'ε', state_mapping[nfa.initial_state.state_id]
        )
        
        # 3. Estados finales originales -> nuevo final
        for final_state_id in nfa.final_states:
            result_nfa.add_transition(
                state_mapping[final_state_id], 'ε', new_final
            )
            
            # 4. Estados finales originales -> inicial original (repetición)
            result_nfa.add_transition(
                state_mapping[final_state_id], 
                'ε', 
                state_mapping[nfa.initial_state.state_id]
            )
        
        return result_nfa
