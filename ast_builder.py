# ast_builder.py (ast_builder.py)

from ast_node import ASTNode


class ASTBuilder:
    """Construye un Árbol de Sintaxis Abstracta a partir de expresiones regulares postfijas"""
    
    def __init__(self):
        self.binary_operators = {'|', '.'}  # Unión y concatenación
        self.unary_operators = {'*'}  # Estrella de Kleene, positivo, opcional
        self.node_counter = 0
    
    def is_escaped_token(self, token):
        """Verifica si un token es un caracter escapado"""
        return len(token) >= 2 and token[0] == '\\'

    def get_escaped_literal(self, token):
        """Extrae el caracter literal de un token escapado"""
        if self.is_escaped_token(token):
            return token[1]
        return token

    def build_ast(self, postfix_expression):
        """
        Construye el AST a partir de una expresión postfija usando una pila
        Retorna: (nodo_raiz, pasos)
        """
        print(postfix_expression, "AAAAAAAAAAAAAAAA", type(postfix_expression))
        stack = []
        steps = []
        self.node_counter = 0
        
        steps.append(f"Construyendo AST desde postfijo: {postfix_expression}")
        steps.append("Pila inicial: []")

        
        for i, token in enumerate(postfix_expression):
            step_info = f"Paso {i+1}: Procesando '{token}'"
            
            if self.is_escaped_token(token):
                literal_value = self.get_escaped_literal(token)
                print("hola soy el literal escapado", literal_value, token)
                node = ASTNode(literal_value, None, None, 'escaped_operand')
                node.original_token = token  # Preservar token original para debug
                node.id = self._get_next_id()
                stack.append(node)

            elif token in self.binary_operators:
                # El operador binario necesita dos operandos
                if len(stack) < 2:
                    raise ValueError(f"No hay suficientes operandos para el operador binario '{token}'")
                
                right = stack.pop()
                left = stack.pop()
                node = ASTNode(token, left, right, 'binary_op')
                node.id = self._get_next_id()
                stack.append(node)
                
                step_info += f" -> Operador binario: pop {right.value} y {left.value}, crear nodo, empujar resultado"
                
            elif token in self.unary_operators:
                # El operador unario necesita un operando
                if len(stack) < 1:
                    raise ValueError(f"No hay suficientes operandos para el operador unario '{token}'")
                
                operand = stack.pop()
                node = ASTNode(token, operand, None, 'unary_op')
                node.id = self._get_next_id()
                stack.append(node)
                
                step_info += f" -> Operador unario: pop {operand.value}, crear nodo, empujar resultado"
                
            else:
                # Operando (carácter o épsilon)
                node = ASTNode(token, None, None, 'operand')
                node.id = self._get_next_id()
                stack.append(node)
                
                step_info += f" -> Operando: crear nodo hoja, empujar a la pila"
            
            # Mostrar el estado actual de la pila
            stack_repr = [node.value for node in stack]
            step_info += f" | Pila: {stack_repr}"
            steps.append(step_info)
        
        if len(stack) != 1:
            raise ValueError("Expresión postfija inválida: la pila debe contener exactamente un elemento")
        
        root = stack[0]
        steps.append(f"Construcción del AST completa. Nodo raíz: {root.value}")
        
        return root, steps
    
    def _get_next_id(self):
        """Genera un ID único para los nodos"""
        self.node_counter += 1
        return f"node_{self.node_counter}"
    
    def print_ast(self, node, level=0, prefix="Root: "):
        """Imprime el AST en un formato similar a un árbol"""
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
