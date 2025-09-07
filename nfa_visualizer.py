# nfa_visualizer.py (nfa_visualizer.py)

import graphviz
from graphviz import escape

class NFAVisualizer:
    """Visualiza AFNs usando Graphviz"""
    
    def __init__(self):
        self.node_styles = {
            'initial': {'shape': 'circle', 'style': 'filled', 'fillcolor': 'lightgreen'},
            'final': {'shape': 'doublecircle', 'style': 'filled', 'fillcolor': 'lightcoral'},
            'initial_final': {'shape': 'doublecircle', 'style': 'filled', 'fillcolor': 'lightblue'},
            'normal': {'shape': 'circle', 'style': 'filled', 'fillcolor': 'lightgray'}
        }
    
    def visualize_nfa(self, nfa, expression_name="NFA"):
        """Crea una representación visual del AFN"""
        dot = graphviz.Digraph(comment=f'AFN para {expression_name}')
        dot.attr(rankdir='LR')  # Diseño de izquierda a derecha
        
        # Establecer atributos del grafo
        dot.attr('graph', {
            'fontname': 'Arial',
            'fontsize': '12',
            'label': f'AFN (Thompson)\n{expression_name}',
            'labelloc': 't'
        })
        
        dot.attr('node', {
            'fontname': 'Arial',
            'fontsize': '10'
        })
        
        dot.attr('edge', {
            'fontname': 'Arial',
            'fontsize': '9'
        })
        
        # Añadir estados
        for state_id, state in nfa.states.items():
            style = self._get_state_style(state, nfa)
            dot.node(f'q{state_id}', escape(f'q{state_id}'), **style)
        
        # Añadir estado fantasma para mostrar el inicial
        if nfa.initial_state:
            dot.node('start', '', shape='point')
            dot.edge('start', f'q{nfa.initial_state.state_id}', label='start')
        
        # Añadir transiciones
        added_edges = set()  # Para evitar aristas duplicadas
        for state_id, state in nfa.states.items():
            for symbol, targets in state.transitions.items():
                for target in targets:
                    edge_key = (state_id, target.state_id, symbol)
                    if edge_key not in added_edges:
                        label = 'ε' if symbol == 'ε' else escape(symbol)
                        dot.edge(f'q{state_id}', f'q{target.state_id}', label=label)
                        added_edges.add(edge_key)
        
        return dot
    
    def _get_state_style(self, state, nfa):
        """Determina el estilo de un estado"""
        is_initial = nfa.initial_state and state.state_id == nfa.initial_state.state_id
        is_final = state.is_final
        
        if is_initial and is_final:
            return self.node_styles['initial_final']
        elif is_initial:
            return self.node_styles['initial']
        elif is_final:
            return self.node_styles['final']
        else:
            return self.node_styles['normal']
    
    def save_and_view(self, dot, filename, view=False):
        """Guarda el grafo y opcionalmente lo visualiza"""
        try:
            dot.render(filename, format='png', cleanup=True)
            print(f"AFN guardado como {filename}.png")
            
            if view:
                dot.view()
            
            return True
        except Exception as e:
            print(f"Error guardando AFN: {e}")
            return False
