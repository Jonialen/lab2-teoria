# nfa.py (nfa.py)

class NFAState:
    """Representa un estado en el AFN"""
    
    def __init__(self, state_id, is_final=False):
        self.state_id = state_id
        self.is_final = is_final
        self.transitions = {}  # {symbol: [list_of_target_states]}
    
    def add_transition(self, symbol, target_state):
        """Añade una transición desde este estado"""
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        if target_state not in self.transitions[symbol]:
            self.transitions[symbol].append(target_state)
    
    def get_transitions(self, symbol):
        """Obtiene las transiciones para un símbolo dado"""
        return self.transitions.get(symbol, [])
    
    def __str__(self):
        return f"State_{self.state_id}{'(F)' if self.is_final else ''}"
    
    def __repr__(self):
        return self.__str__()


class NFA:
    """Representa un Autómata Finito No-determinista"""
    
    def __init__(self):
        self.states = {}  # {state_id: NFAState}
        self.initial_state = None
        self.final_states = set()
        self.alphabet = set()
        self.state_counter = 0
    
    def create_state(self, is_final=False):
        """Crea un nuevo estado"""
        state_id = self.state_counter
        self.state_counter += 1
        state = NFAState(state_id, is_final)
        self.states[state_id] = state
        
        if is_final:
            self.final_states.add(state_id)
        
        return state
    
    def set_initial_state(self, state):
        """Establece el estado inicial"""
        self.initial_state = state
    
    def add_transition(self, from_state, symbol, to_state):
        """Añade una transición entre estados"""
        from_state.add_transition(symbol, to_state)
        if symbol != 'ε':  # No añadir epsilon al alfabeto
            self.alphabet.add(symbol)
    
    def get_epsilon_closure(self, states):
        """Calcula la epsilon-clausura de un conjunto de estados"""
        closure = set(states)
        stack = list(states)
        
        while stack:
            current_state = stack.pop()
            epsilon_transitions = current_state.get_transitions('ε')
            
            for next_state in epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        
        return closure
    
    def get_states_info(self):
        """Obtiene información resumida de los estados"""
        info = {
            'total_states': len(self.states),
            'initial_state': self.initial_state.state_id if self.initial_state else None,
            'final_states': list(self.final_states),
            'alphabet': list(self.alphabet)
        }
        return info
