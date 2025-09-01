# ast_node.py (ast_node.py)

class ASTNode:
    """Representa un nodo en el Árbol de Sintaxis Abstracta para expresiones regulares"""
    
    def __init__(self, value, left=None, right=None, node_type='operand'):
        self.value = value
        self.left = left
        self.right = right
        self.node_type = node_type  # 'operando', 'op_unario', 'op_binario'
        self.id = None  # Para visualización con Graphviz
    
    def is_leaf(self):
        """Comprueba si este nodo es una hoja (operando)"""
        return self.left is None and self.right is None
    
    def __str__(self):
        return f"Node({self.value})"
    
    def __repr__(self):
        return self.__str__()