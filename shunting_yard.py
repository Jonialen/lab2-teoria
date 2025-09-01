# shunting_yard.py (shunting_yard.py)

from expression_balancer import ExpressionBalancer

class ShuntingYard:
    """
    Implementa el algoritmo de Shunting Yard para convertir expresiones regulares
    de notación infix a postfix en forma atómica para el algoritmo de Thompson.
    """

    def __init__(self):
        self.precedence = {
            '|': 1,  # alternancia
            '.': 2,  # concatenación
            '*': 3,  # clausura de Kleene
        }
        # Solo operadores atómicos para Thompson
        self.atomic_ops = {'|', '.', '*'}
        # Inicializar el balanceador
        self.balancer = ExpressionBalancer()

    def tokenize(self, regex):
        """Tokeniza manejando caracteres escapados y clases de caracteres [...]"""
        tokens = []
        i = 0
        
        while i < len(regex):
            if regex[i] == '\\' and i + 1 < len(regex):
                # Carácter escapado: '\x' como un token literal
                tokens.append(regex[i:i+2])
                i += 2
            elif regex[i] == '[':
                # Inicio de una clase de caracteres
                j = i + 1
                # Buscar el ']' correspondiente
                while j < len(regex) and regex[j] != ']':
                    j += 1
                
                if j < len(regex):
                    # Clase de caracteres encontrada
                    tokens.append(regex[i:j+1])
                    i = j + 1
                else:
                    # Si no se encuentra ']', tratar '[' como literal
                    tokens.append(regex[i])
                    i += 1
            else:
                tokens.append(regex[i])
                i += 1
        
        return tokens

    def expand_character_classes(self, tokens):
        """Expande clases de caracteres [abc] a (a|b|c)"""
        expanded_tokens = []
        for token in tokens:
            if token.startswith('[') and token.endswith(']'):
                # Es una clase de caracteres
                chars = token[1:-1]
                if not chars:
                    # Clase vacía, podría ser un error o un caso especial
                    # Por ahora, lo omitimos o manejamos como un literal vacío si es necesario
                    continue

                # Construir la expresión de alternancia
                expanded_tokens.append('(')
                for i, char in enumerate(chars):
                    # Manejar posibles caracteres escapados dentro de la clase si es necesario
                    # Por simplicidad, aquí tratamos cada carácter como literal
                    expanded_tokens.append(char)
                    if i < len(chars) - 1:
                        expanded_tokens.append('|')
                expanded_tokens.append(')')
            else:
                expanded_tokens.append(token)
        return expanded_tokens

    def is_literal(self, token):
        """Verifica si un token es un literal (operando)"""
        if len(token) == 2 and token[0] == '\\':
            return True  # Carácter escapado
        if len(token) == 1 and token.isalnum():
            return True  # Letra o número
        if token == 'ε':
            return True  # Epsilon
        return False

    def extract_operand_from_end(self, tokens):
        """
        Extrae el operando completo del final de la lista de tokens.
        Retorna (operand_tokens, remaining_tokens)
        """
        if not tokens:
            return [], tokens
        
        # Si el último token es ')', buscar la expresión balanceada
        if tokens[-1] == ')':
            level = 1
            i = len(tokens) - 2
            
            while i >= 0 and level > 0:
                if tokens[i] == ')':
                    level += 1
                elif tokens[i] == '(':
                    level -= 1
                i -= 1
            
            if level == 0:  # Expresión balanceada encontrada
                operand = tokens[i + 1:]  # Desde '(' hasta ')'
                remaining = tokens[:i + 1]
                return operand, remaining
        
        # Si es un token literal simple
        if self.is_literal(tokens[-1]):
            return [tokens[-1]], tokens[:-1]
        
        # Fallback: último token
        return [tokens[-1]], tokens[:-1]

    def expand_plus_and_question(self, tokens):
        """
        Convierte + y ? a su forma atómica:
        - a+ -> a a *  (concatenación de a con a*)
        - a? -> ( ε | a )  (alternancia entre ε y a)
        """
        result = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            if token == '+' and result:
                # Extraer operando: a+ -> aa*
                operand, remaining = self.extract_operand_from_end(result)
                if operand:
                    result = remaining  # Quitar operando original
                    result.extend(operand)  # a
                    result.extend(operand)  # a (segunda copia)
                    result.append('*')      # *
                else:
                    result.append(token)  # Si no hay operando, mantener +
                
            elif token == '?' and result:
                # Extraer operando: a? -> (ε|a)
                operand, remaining = self.extract_operand_from_end(result)
                if operand:
                    result = remaining  # Quitar operando original
                    result.append('(')  # (
                    result.append('ε')  # ε
                    result.append('|')  # |
                    result.extend(operand)  # a
                    result.append(')')  # )
                else:
                    result.append(token)  # Si no hay operando, mantener ?
                    
            else:
                result.append(token)
            
            i += 1
        
        return result

    def add_concatenation(self, tokens):
        """Inserta concatenación explícita entre tokens apropiados"""
        if not tokens:
            return tokens
            
        result = []
        
        for i in range(len(tokens)):
            result.append(tokens[i])
            
            # Solo insertar '.' si no es el último token
            if i < len(tokens) - 1:
                curr = tokens[i]
                next_token = tokens[i + 1]
                
                should_concat = (
                    # literal seguido de literal: ab
                    (self.is_literal(curr) and self.is_literal(next_token)) or
                    # literal seguido de '(': a(
                    (self.is_literal(curr) and next_token == '(') or
                    # ')' seguido de literal: )a  
                    (curr == ')' and self.is_literal(next_token)) or
                    # ')' seguido de '(': )(
                    (curr == ')' and next_token == '(') or
                    # '*' seguido de literal: a*b
                    (curr == '*' and self.is_literal(next_token)) or
                    # '*' seguido de '(': a*(
                    (curr == '*' and next_token == '(')
                )
                
                if should_concat:
                    result.append('.')
        
        return result

    def infix_to_postfix(self, infix):
        """Convierte a postfix usando solo operadores atómicos para Thompson"""
        steps = []
        steps.append(f"Original: {infix}")
        
        # Verificar balance ANTES de procesar
        is_balanced, balance_steps = self.balancer.is_balanced(infix)
        steps.extend([f"[Balance] {step}" for step in balance_steps])
        
        if not is_balanced:
            steps.append("EXPRESIÓN NO BALANCEADA - CONVERSIÓN OMITIDA")
            return None, steps
        
        steps.append("Expresión balanceada - Procediendo con conversión")
        
        # Paso 1: Tokenizar
        tokens = self.tokenize(infix)
        steps.append(f"Tokens: {tokens}")
        
        # Paso 2: Expandir + y ? a forma atómica
        atomic_tokens = self.expand_plus_and_question(tokens)
        steps.append(f"Forma atómica: {atomic_tokens}")
        
        # Paso 3: Agregar concatenación explícita
        tokens_with_concat = self.add_concatenation(atomic_tokens)
        steps.append(f"Con concatenación: {tokens_with_concat}")
        
        # Paso 4: Aplicar Shunting Yard
        output = []
        stack = []
        steps.append("Iniciando Shunting Yard:")
        
        for i, token in enumerate(tokens_with_concat):
            step_info = f"  Paso {i+1}: '{token}'"
            
            if self.is_literal(token):
                # Operandos van directamente a la salida
                output.append(token)
                step_info += f" -> Operando a salida: {output}"
                
            elif token == '*':
                # * es operador unario postfijo, va directo a salida
                output.append(token)
                step_info += f" -> Operador * a salida: {output}"
                
            elif token in {'|', '.'}:
                # Operadores binarios: aplicar reglas de precedencia
                while (stack and 
                       stack[-1] != '(' and 
                       stack[-1] in self.atomic_ops and
                       self.precedence[stack[-1]] >= self.precedence[token]):
                    output.append(stack.pop())
                stack.append(token)
                step_info += f" -> Pila: {stack}, Salida: {output}"
                
            elif token == '(':
                stack.append(token)
                step_info += f" -> '(' a pila: {stack}"
                
            elif token == ')':
                # Vaciar hasta encontrar '('
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack:
                    stack.pop()  # Remover '('
                step_info += f" -> Vaciar hasta '(': Pila: {stack}, Salida: {output}"
            
            steps.append(step_info)
        
        # Vaciar stack restante
        while stack:
            output.append(stack.pop())
        
        postfix = ''.join(output)
        steps.append(f"Postfija final: {postfix}")
        
        return postfix, steps

    def process_expressions(self, expressions):
        """
        Procesa una lista de expresiones, mostrando pasos y resultados.
        """
        results = []
        
        for idx, expression in enumerate(expressions, 1):
            print(f"\n{'='*60}")
            print(f"EXPRESIÓN {idx}: {expression}")
            print('='*60)
            
            postfix, steps = self.infix_to_postfix(expression)
            
            for step in steps:
                print(f"  {step}")
            
            if postfix:
                print(f"RESULTADO FINAL: {postfix}")
                results.append(f"{expression} -> {postfix}")
            else:
                print(f"EXPRESIÓN OMITIDA POR NO ESTAR BALANCEADA")
                results.append(f"{expression} -> NO BALANCEADA, OMITIDA")
            
            print("-" * 60)
        
        return results

    def process_file(self, filename):
        """
        Procesa expresiones desde un archivo.
        Compatible con la interfaz requerida por main.py
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
            
            print(f"Procesando archivo: {filename}")
            print(f"Expresiones encontradas: {len(lines)}")
            
            if not lines:
                print("Archivo vacío o sin expresiones válidas")
                return ["Archivo vacío o sin expresiones válidas"]
            
            return self.process_expressions(lines)
            
        except FileNotFoundError:
            error_msg = f"Error: Archivo '{filename}' no encontrado."
            print(error_msg)
            return [error_msg]
        except Exception as e:
            error_msg = f"Error procesando archivo: {e}"
            print(error_msg)
            return [error_msg]


def main():
    """Función principal para pruebas independientes"""
    print("=== ALGORITMO SHUNTING YARD PARA THOMPSON ===")
    print("Convierte expresiones regulares a forma atómica postfija.\n")
    
    converter = ShuntingYard()
    
    # Casos de prueba
    test_expressions = [
        "a+",           # Caso simple +
        "a?",           # Caso simple ?
        "\\++",         # Carácter literal + con operador +
        "(a|b)+",       # Expresión compleja con +
        "(a|b)?",       # Expresión compleja con ?
        "a+b*c?",       # Múltiples operadores
        "((a|b)*c)+",   # Anidamiento complejo
        "a(b+",         # No balanceada (debe fallar)
    ]
    
    print("CASOS DE PRUEBA:")
    results = converter.process_expressions(test_expressions)
    
    print(f"\n{'='*60}")
    print("PROCESANDO ARCHIVO expressions.txt:")
    file_results = converter.process_file('expressions.txt')
    
    # Mostrar resumen
    print(f"\n{'='*60}")
    print("RESUMEN DE RESULTADOS:")
    print('='*60)
    all_results = results + file_results
    for result in all_results:
        print(f"  {result}")


if __name__ == "__main__":
    main()
