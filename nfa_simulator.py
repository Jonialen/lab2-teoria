# nfa_simulator.py (nfa_simulator.py)

class NFASimulator:
    """Simula la ejecución de un AFN para verificar cadenas"""
    
    def __init__(self, nfa):
        self.nfa = nfa
    
    def simulate(self, input_string):
        """
        Simula el AFN con una cadena de entrada
        Retorna (aceptado, pasos)
        """
        steps = []
        steps.append(f"Simulando AFN con cadena: '{input_string}'")
        steps.append(f"Estado inicial: q{self.nfa.initial_state.state_id}")
        
        # Comenzar con la clausura épsilon del estado inicial
        current_states = self.nfa.get_epsilon_closure([self.nfa.initial_state])
        state_names = [f'q{s.state_id}' for s in current_states]
        steps.append(f"Estados tras clausura épsilon inicial: {{{', '.join(state_names)}}}")
        
        # Procesar cada carácter
        for i, symbol in enumerate(input_string):
            steps.append(f"\nPaso {i+1}: Procesando símbolo '{symbol}'")
            steps.append(f"Estados actuales: {{{', '.join([f'q{s.state_id}' for s in current_states])}}}")
            
            next_states = set()
            
            # Para cada estado actual, encontrar transiciones con el símbolo
            for state in current_states:
                transitions = state.get_transitions(symbol)
                for target in transitions:
                    next_states.add(target)
                    steps.append(f"  Transición: q{state.state_id} --{symbol}--> q{target.state_id}")
            
            if not next_states:
                steps.append(f"  No hay transiciones para '{symbol}' desde los estados actuales")
                steps.append("CADENA RECHAZADA: No hay más transiciones")
                return False, steps
            
            # Aplicar clausura épsilon
            current_states = self.nfa.get_epsilon_closure(list(next_states))
            state_names = [f'q{s.state_id}' for s in current_states]
            steps.append(f"  Estados tras transiciones y clausura épsilon: {{{', '.join(state_names)}}}")
        
        # Verificar si algún estado actual es final
        final_states_reached = [s for s in current_states if s.is_final]
        
        steps.append(f"\nEstados finales del AFN: {{{', '.join([f'q{s}' for s in self.nfa.final_states])}}}")
        steps.append(f"Estados actuales: {{{', '.join([f'q{s.state_id}' for s in current_states])}}}")
        
        if final_states_reached:
            final_names = [f'q{s.state_id}' for s in final_states_reached]
            steps.append(f"Estados finales alcanzados: {{{', '.join(final_names)}}}")
            steps.append("CADENA ACEPTADA")
            return True, steps
        else:
            steps.append("No se alcanzó ningún estado final")
            steps.append("CADENA RECHAZADA")
            return False, steps