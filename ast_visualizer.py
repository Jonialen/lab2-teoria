# ast_visualizer.py (ast_visualizer.py)

import graphviz
from ast_node import ASTNode


class ASTVisualizer:
    """Visualiza Árboles de Sintaxis Abstracta usando Graphviz"""
    
    def __init__(self):
        self.node_styles = {
            'operand': {'shape': 'circle', 'style': 'filled', 'fillcolor': 'lightblue'},
            'binary_op': {'shape': 'diamond', 'style': 'filled', 'fillcolor': 'lightgreen'},
            'unary_op': {'shape': 'square', 'style': 'filled', 'fillcolor': 'lightyellow'}
        }
    
    def visualize_ast(self, root, expression_name="AST", save_format='png'):
        """
        Crea una representación visual del AST
        Returns: graphviz.Digraph object
        """
        dot = graphviz.Digraph(comment=f'AST para {expression_name}')
        dot.attr(rankdir='TB')  # Diseño de arriba hacia abajo
        
        # Establecer atributos del grafo para una mejor visualización
        dot.attr('graph', {
            'fontname': 'Arial',
            'fontsize': '12',
            'label': f'AST\n{expression_name}',
            'labelloc': 't'
        })
        
        dot.attr('node', {
            'fontname': 'Arial',
            'fontsize': '10',
            'width': '0.5',
            'height': '0.5'
        })
        
        # Añadir nodos y aristas recursivamente
        self._add_nodes_and_edges(dot, root)
        
        return dot
    
    def _add_nodes_and_edges(self, dot, node):
        """Añade nodos y aristas recursivamente al grafo"""
        if node is None:
            return
        
        # Obtener el estilo del nodo según el tipo
        style = self.node_styles.get(node.node_type, {})
        
        # Manejar caracteres especiales para su visualización
        display_value = self._format_node_value(node.value)
        
        # Añadir el nodo
        dot.node(node.id, display_value, **style)
        
        # Añadir aristas a los hijos
        if node.left:
            self._add_nodes_and_edges(dot, node.left)
            dot.edge(node.id, node.left.id, label='I')
        
        if node.right:
            self._add_nodes_and_edges(dot, node.right)
            dot.edge(node.id, node.right.id, label='D')
    
    def _format_node_value(self, value):
        """Formatea los valores de los nodos para una mejor visualización"""
        special_chars = {
            '|': '∪',  # Símbolo de unión
            '.': '•',  # Símbolo de concatenación
            '*': '*',  # Estrella de Kleene
            '+': '+',  # Uno o más
            '?': '?',  # Opcional
            'ε': 'ε'  # Épsilon
        }
        return special_chars.get(value, value)
    
    def save_and_view(self, dot, filename, view=True):
        """Guarda el grafo y opcionalmente lo visualiza"""
        try:
            # Guardar como PNG
            dot.render(filename, format='png', cleanup=True)
            print(f"AST guardado como {filename}.png")
            
            if view:
                dot.view()
            
            return True
        except Exception as e:
            print(f"Error guardando AST: {e}")
            return False
