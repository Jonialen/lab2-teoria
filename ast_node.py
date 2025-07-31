# ast_node.py (ast_node.py)

class ASTNode:
    """Represents a node in the Abstract Syntax Tree for regular expressions"""
    
    def __init__(self, value, left=None, right=None, node_type='operand'):
        self.value = value
        self.left = left
        self.right = right
        self.node_type = node_type  # 'operand', 'unary_op', 'binary_op'
        self.id = None  # For Graphviz visualization
    
    def is_leaf(self):
        """Check if this node is a leaf (operand)"""
        return self.left is None and self.right is None
    
    def __str__(self):
        return f"Node({self.value})"
    
    def __repr__(self):
        return self.__str__()
