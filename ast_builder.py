# ast_builder.py (ast_builder.py)

from ast_node import ASTNode


class ASTBuilder:
    """Builds Abstract Syntax Tree from postfix regular expressions"""
    
    def __init__(self):
        self.binary_operators = {'|', '.'}  # Union and concatenation
        self.unary_operators = {'*', '+', '?'}  # Kleene star, plus, optional
        self.node_counter = 0
    
    def build_ast(self, postfix_expression):
        """
        Build AST from postfix expression using a stack
        Returns: (root_node, steps)
        """
        stack = []
        steps = []
        self.node_counter = 0
        
        steps.append(f"Building AST from postfix: {postfix_expression}")
        steps.append("Initial stack: []")
        
        for i, token in enumerate(postfix_expression):
            step_info = f"Step {i+1}: Processing '{token}'"
            
            if token in self.binary_operators:
                # Binary operator needs two operands
                if len(stack) < 2:
                    raise ValueError(f"Not enough operands for binary operator '{token}'")
                
                right = stack.pop()
                left = stack.pop()
                node = ASTNode(token, left, right, 'binary_op')
                node.id = self._get_next_id()
                stack.append(node)
                
                step_info += f" -> Binary operator: pop {right.value} and {left.value}, create node, push result"
                
            elif token in self.unary_operators:
                # Unary operator needs one operand
                if len(stack) < 1:
                    raise ValueError(f"Not enough operands for unary operator '{token}'")
                
                operand = stack.pop()
                node = ASTNode(token, operand, None, 'unary_op')
                node.id = self._get_next_id()
                stack.append(node)
                
                step_info += f" -> Unary operator: pop {operand.value}, create node, push result"
                
            else:
                # Operand (character or epsilon)
                node = ASTNode(token, None, None, 'operand')
                node.id = self._get_next_id()
                stack.append(node)
                
                step_info += f" -> Operand: create leaf node, push to stack"
            
            # Show current stack state
            stack_repr = [node.value for node in stack]
            step_info += f" | Stack: {stack_repr}"
            steps.append(step_info)
        
        if len(stack) != 1:
            raise ValueError("Invalid postfix expression: stack should contain exactly one element")
        
        root = stack[0]
        steps.append(f"AST construction complete. Root node: {root.value}")
        
        return root, steps
    
    def _get_next_id(self):
        """Generate unique ID for nodes"""
        self.node_counter += 1
        return f"node_{self.node_counter}"
    
    def print_ast(self, node, level=0, prefix="Root: "):
        """Print AST in a tree-like format"""
        if node is None:
            return
        
        print("  " * level + prefix + str(node.value))
        
        if node.left or node.right:
            if node.left:
                self.print_ast(node.left, level + 1, "L--- ")
            else:
                print("  " * (level + 1) + "L--- None")
                
            if node.right:
                self.print_ast(node.right, level + 1, "R--- ")
            else:
                print("  " * (level + 1) + "R--- None")
