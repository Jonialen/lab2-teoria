# ast_visualizer.py (ast_visualizer.py)

import graphviz
from ast_node import ASTNode


class ASTVisualizer:
    """Visualizes Abstract Syntax Trees using Graphviz"""
    
    def __init__(self):
        self.node_styles = {
            'operand': {'shape': 'circle', 'style': 'filled', 'fillcolor': 'lightblue'},
            'binary_op': {'shape': 'diamond', 'style': 'filled', 'fillcolor': 'lightgreen'},
            'unary_op': {'shape': 'square', 'style': 'filled', 'fillcolor': 'lightyellow'}
        }
    
    def visualize_ast(self, root, expression_name="AST", save_format='png'):
        """
        Create a visual representation of the AST
        Returns: graphviz.Digraph object
        """
        dot = graphviz.Digraph(comment=f'AST for {expression_name}')
        dot.attr(rankdir='TB')  # Top to bottom layout
        
        # Set graph attributes for better visualization
        dot.attr('graph', {
            'fontname': 'Arial',
            'fontsize': '12',
            'label': f'Abstract Syntax Tree\\n{expression_name}',
            'labelloc': 't'
        })
        
        dot.attr('node', {
            'fontname': 'Arial',
            'fontsize': '10',
            'width': '0.5',
            'height': '0.5'
        })
        
        # Add nodes and edges recursively
        self._add_nodes_and_edges(dot, root)
        
        return dot
    
    def _add_nodes_and_edges(self, dot, node):
        """Recursively add nodes and edges to the graph"""
        if node is None:
            return
        
        # Get node style based on type
        style = self.node_styles.get(node.node_type, {})
        
        # Handle special characters for display
        display_value = self._format_node_value(node.value)
        
        # Add the node
        dot.node(node.id, display_value, **style)
        
        # Add edges to children
        if node.left:
            self._add_nodes_and_edges(dot, node.left)
            dot.edge(node.id, node.left.id, label='L')
        
        if node.right:
            self._add_nodes_and_edges(dot, node.right)
            dot.edge(node.id, node.right.id, label='R')
    
    def _format_node_value(self, value):
        """Format node values for better display"""
        special_chars = {
            '|': '∪',  # Union symbol
            '.': '•',  # Concatenation symbol
            '*': '*',  # Kleene star
            '+': '+',  # One or more
            '?': '?',  # Optional
            'ε': 'ε',  # Epsilon
        }
        return special_chars.get(value, value)
    
    def save_and_view(self, dot, filename, view=True):
        """Save the graph and optionally view it"""
        try:
            # Save as PNG
            dot.render(filename, format='png', cleanup=True)
            print(f"AST saved as {filename}.png")
            
            if view:
                dot.view()
            
            return True
        except Exception as e:
            print(f"Error saving AST: {e}")
            return False
