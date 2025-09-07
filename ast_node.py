# ast_node.py (ast_node.py)

class ASTNode:
    """Representa un nodo en el Árbol de Sintaxis Abstracta para expresiones regulares"""
    
    def __init__(self, value, left=None, right=None, node_type='operand'):
        self.value = value
        self.left = left
        self.right = right
        self.node_type = node_type  # 'operando', 'op_unario', 'op_binario', 'escaped_operand'
        self.original_token = None
        self.id = None  # Para visualización con Graphviz
    
    def is_leaf(self):
        """Comprueba si este nodo es una hoja (operando)"""
        return self.left is None and self.right is None

    def is_escaped_literal(self):
        """Comprueba si este nodo representa un carácter escapado"""
        return self.node_type == 'escaped_operand'

    def get_display_value(self):
        """Obtiene el valor para mostrar, incluyendo escape si aplica"""
        if self.is_escaped_literal() and self.original_token:
            return self.original_token  # Mostrar '\|' en lugar de '|'
        return self.value
    
    def __str__(self):
        return f"Node({self.value})"
    
    def __repr__(self):
        return self.__str__()
