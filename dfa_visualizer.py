# dfa_visualizer.py (dfa_visualizer.py)

import graphviz


class DFAVisualizer:
    """Visualiza AFDs usando Graphviz"""
    
    def __init__(self):
        self.node_styles = {
            'initial': {'shape': 'circle', 'style': 'filled', 'fillcolor': 'lightgreen'},
            'final': {'shape': 'doublecircle', 'style': 'filled', 'fillcolor': 'lightcoral'},
            'initial_final': {'shape': 'doublecircle', 'style': 'filled', 'fillcolor': 'lightblue'},
            'normal': {'shape': 'circle', 'style': 'filled', 'fillcolor': 'lightgray'}
        }
    
    def visualize_dfa(self, dfa, expression_name="AFD", show_nfa_states=False):
        """Crea una representación visual del AFD"""
        dot = graphviz.Digraph(comment=f'AFD para {expression_name}')
        dot.attr(rankdir='LR')  # Diseño de izquierda a derecha
        
        # Establecer atributos del grafo
        dot.attr('graph', {
            'fontname': 'Arial',
            'fontsize': '12',
            'label': f'AFD (Construcción de Subconjuntos)\n{expression_name}',
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
        for state_id, state in dfa.states.items():
            style = self._get_state_style(state, dfa)
            label = self._create_state_label(state, show_nfa_states)
            dot.node(f'q{state_id}', graphviz.escape(label), **style)
        
        # Añadir estado fantasma para mostrar el inicial
        if dfa.initial_state:
            dot.node('start', '', shape='point')
            dot.edge('start', f'q{dfa.initial_state.state_id}', label='start')
        
        # Añadir transiciones
        for state_id, state in dfa.states.items():
            for symbol, target_state in state.transitions.items():
                dot.edge(f'q{state_id}', f'q{target_state.state_id}', label=graphviz.escape(symbol))
        
        return dot
    
    def _get_state_style(self, state, dfa):
        """Determina el estilo de un estado"""
        is_initial = dfa.initial_state and state.state_id == dfa.initial_state.state_id
        is_final = state.is_final
        
        if is_initial and is_final:
            return self.node_styles['initial_final']
        elif is_initial:
            return self.node_styles['initial']
        elif is_final:
            return self.node_styles['final']
        else:
            return self.node_styles['normal']
    
    def _create_state_label(self, state, show_nfa_states=False):
        """Crea la etiqueta de un estado del AFD"""
        base_label = f'q{state.state_id}'
        
        if show_nfa_states and state.nfa_states:
            nfa_ids = sorted(s.state_id for s in state.nfa_states)
            nfa_label = '{' + ','.join(map(str, nfa_ids)) + '}'
            return f'{base_label}\\n{nfa_label}'
        
        return base_label
    
    def save_and_view(self, dot, filename, view=False):
        """Guarda el grafo y opcionalmente lo visualiza"""
        try:
            dot.render(filename, format='png', cleanup=True)
            print(f"AFD guardado como {filename}.png")
            
            if view:
                dot.view()
            
            return True
        except Exception as e:
            print(f"Error guardando AFD: {e}")
            return False


def test_dfa_visualizer():
    """Función de prueba para el visualizador de AFD simplificado"""
    print("=== PRUEBA DEL VISUALIZADOR DE AFD SIMPLIFICADO ===")
    
    # Importar dependencias
    from shunting_yard import ShuntingYard
    from ast_builder import ASTBuilder
    from thompson import ThompsonConstructor
    from subset_construction import SubsetConstruction
    
    # Expresión de prueba
    test_expr = "(a|b)*a"
    print(f"Expresión de prueba: {test_expr}")
    
    # Pipeline completo
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
    
    # Crear visualizador
    visualizer = DFAVisualizer()
    
    print(f"Creando visualizaciones...")
    
    # 1. AFD simple (sin mostrar estados del AFN)
    dfa_dot = visualizer.visualize_dfa(dfa, f"{test_expr}")
    visualizer.save_and_view(dfa_dot, "test_afd_simple", view=False)
    
    # 2. AFD con estados del AFN mostrados
    dfa_with_nfa_dot = visualizer.visualize_dfa(dfa, f"{test_expr}", show_nfa_states=True)
    visualizer.save_and_view(dfa_with_nfa_dot, "test_afd_con_afn", view=False)
    
    print(f"Visualizaciones creadas:")
    print(f"  - test_afd_simple.png (AFD simple)")
    print(f"  - test_afd_con_afn.png (AFD con estados del AFN)")


if __name__ == "__main__":
    test_dfa_visualizer()

