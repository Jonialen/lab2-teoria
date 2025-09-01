# dfa.py (dfa.py)

class DFAState:
    """Representa un estado en el AFD"""
    
    def __init__(self, state_id, nfa_states_set=None, is_final=False):
        self.state_id = state_id
        self.nfa_states = nfa_states_set if nfa_states_set else set()  # Conjunto de estados del AFN
        self.is_final = is_final
        self.transitions = {}  # {symbol: target_state} - Determinista
        self.name = f"q{state_id}"  # Nombre para visualización
    
    def add_transition(self, symbol, target_state):
        """Añade una transición desde este estado (determinista)"""
        self.transitions[symbol] = target_state
    
    def get_transition(self, symbol):
        """Obtiene la transición para un símbolo dado"""
        return self.transitions.get(symbol, None)
    
    def contains_nfa_state(self, nfa_state_id):
        """Verifica si este estado del AFD contiene un estado específico del AFN"""
        return nfa_state_id in [s.state_id for s in self.nfa_states]
    
    def get_nfa_state_ids(self):
        """Obtiene los IDs de los estados del AFN que representa este estado"""
        return sorted([s.state_id for s in self.nfa_states])
    
    def __str__(self):
        nfa_ids = self.get_nfa_state_ids()
        return f"q{self.state_id}({{{','.join(map(str, nfa_ids))}}})"
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(tuple(sorted(s.state_id for s in self.nfa_states)))
    
    def __eq__(self, other):
        if not isinstance(other, DFAState):
            return False
        return set(s.state_id for s in self.nfa_states) == set(s.state_id for s in other.nfa_states)


class DFA:
    """Representa un Autómata Finito Determinista"""
    
    def __init__(self):
        self.states = {}  # {state_id: DFAState}
        self.initial_state = None
        self.final_states = set()  # Set of state_ids
        self.alphabet = set()
        self.state_counter = 0
        
    def create_state(self, nfa_states_set=None, is_final=False):
        """Crea un nuevo estado del AFD"""
        state_id = self.state_counter
        self.state_counter += 1
        state = DFAState(state_id, nfa_states_set, is_final)
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
        if symbol != 'ε':  # No añadir epsilon al alfabeto del AFD
            self.alphabet.add(symbol)
    
    def get_state_by_nfa_set(self, nfa_states_set):
        """Busca un estado del AFD que represente el mismo conjunto de estados del AFN"""
        nfa_state_ids = set(s.state_id for s in nfa_states_set)
        
        for state in self.states.values():
            state_nfa_ids = set(s.state_id for s in state.nfa_states)
            if nfa_state_ids == state_nfa_ids:
                return state
        return None
    
    def has_state_with_nfa_set(self, nfa_states_set):
        """Verifica si ya existe un estado que represente este conjunto de estados del AFN"""
        return self.get_state_by_nfa_set(nfa_states_set) is not None
    
    def get_states_info(self):
        """Obtiene información resumida de los estados"""
        info = {
            'total_states': len(self.states),
            'initial_state': self.initial_state.state_id if self.initial_state else None,
            'final_states': list(self.final_states),
            'alphabet': list(self.alphabet)
        }
        return info
    
    def print_transitions(self):
        """Imprime todas las transiciones del AFD"""
        print("Transiciones del AFD:")
        for state_id, state in self.states.items():
            for symbol, target in state.transitions.items():
                print(f"  {state} --{symbol}--> {target}")
    
    def get_reachable_states(self):
        """Obtiene todos los estados alcanzables desde el estado inicial"""
        if not self.initial_state:
            return set()
        
        reachable = set()
        stack = [self.initial_state]
        
        while stack:
            current = stack.pop()
            if current.state_id not in reachable:
                reachable.add(current.state_id)
                for target in current.transitions.values():
                    if target.state_id not in reachable:
                        stack.append(target)
        
        return reachable
