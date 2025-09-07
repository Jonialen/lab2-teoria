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

    def expand_range(self, start_char, end_char):
        """
        Expande un rango de caracteres como 'a-z' o '0-9'
        Returns: lista de caracteres o None si el rango no es válido
        """
        # Verificar que ambos sean caracteres individuales
        if len(start_char) != 1 or len(end_char) != 1:
            return None
        
        start_ord = ord(start_char)
        end_ord = ord(end_char)
        
        # El rango debe ser válido (start <= end)
        if start_ord > end_ord:
            return None
        
        # Verificar que sean del mismo tipo para rangos comunes
        if (start_char.isalpha() and end_char.isalpha()) or \
           (start_char.isdigit() and end_char.isdigit()) or \
           (start_char.isalnum() and end_char.isalnum()):
            # Generar todos los caracteres en el rango
            return [chr(i) for i in range(start_ord, end_ord + 1)]
        
        # Para otros casos, también permitir el rango si es secuencial
        return [chr(i) for i in range(start_ord, end_ord + 1)]

    def parse_character_class(self, chars_inside):
        """
        Parsea el contenido de una clase de caracteres [...]
        Maneja rangos como a-z, caracteres literales y combinaciones
        """
        if not chars_inside:
            return []
        
        characters = set()  # Usar set para evitar duplicados
        i = 0
        
        while i < len(chars_inside):
            # Caso especial: guión al principio o al final es literal
            if chars_inside[i] == '-' and (i == 0 or i == len(chars_inside) - 1):
                characters.add('-')
                i += 1
                continue
            
            # Verificar si hay un rango: x-y
            if i + 2 < len(chars_inside) and chars_inside[i + 1] == '-':
                start_char = chars_inside[i]
                end_char = chars_inside[i + 2]
                
                # Intentar expandir el rango
                range_chars = self.expand_range(start_char, end_char)
                
                if range_chars:
                    # Rango válido, agregar todos los caracteres
                    characters.update(range_chars)
                    i += 3  # Saltar start_char, -, end_char
                else:
                    # Rango inválido, tratar como caracteres literales
                    characters.add(start_char)
                    i += 1
            else:
                # Carácter literal
                characters.add(chars_inside[i])
                i += 1
        
        return sorted(list(characters))  # Retornar lista ordenada

    def tokenize(self, regex):
        """Tokeniza manejando caracteres escapados"""
        tokens = []
        i = 0
        
        while i < len(regex):
            if regex[i] == '\\' and i + 1 < len(regex):
                # Carácter escapado: '\x' como un token literal
                tokens.append(regex[i:i+2])
                i += 2
            elif regex[i] == ".":
                tokens.append('\\'+regex[i])
                i += 1
            else:
                tokens.append(regex[i])
                i += 1
        
        print("hola soy los tokens", tokens)
        return tokens

    def is_literal(self, token):
        """Verifica si un token es un literal (operando)"""
        # Carácter escapado (siempre literal)
        if len(token) >= 2 and token[0] == '\\':
            return True
        
        # Epsilon
        if token == 'ε':
            return True
        
        # Un solo carácter que no sea operador
        if len(token) == 1 and token not in {'|', '.', '*', '(', ')', '[', ']'}:
            return True
        
        return False

    def expand_character_classes(self, tokens):
        """
        Expande clases de caracteres [abc] a alternancia (a|b|c)
        Trabaja con tokens ya tokenizados para manejar escapes correctamente
        """
        result = []
        i = 0
        
        while i < len(tokens):
            if tokens[i] == '[':
                # Buscar el cierre del corchete
                j = i + 1
                bracket_level = 1
                
                while j < len(tokens) and bracket_level > 0:
                    if tokens[j] == '[':
                        bracket_level += 1
                    elif tokens[j] == ']':
                        bracket_level -= 1
                    j += 1
                
                if bracket_level == 0:  # Encontró el cierre balanceado
                    # Extraer tokens dentro de los corchetes
                    chars_inside = tokens[i+1:j-1]
                    
                    # Convertir tokens a string para parsear rangos
                    chars_str = ''.join(chars_inside)
                    expanded_chars = self.parse_character_class(chars_str)
                    
                    if expanded_chars:
                        # Crear alternancia: (a|b|c)
                        result.append('(')
                        for k, char in enumerate(expanded_chars):
                            if k > 0:
                                result.append('|')
                            result.append(char)
                        result.append(')')
                    else:
                        # Clase vacía, mantener tokens originales
                        result.extend(tokens[i:j])
                    
                    i = j
                else:
                    # No balanceado, mantener como literal
                    result.append(tokens[i])
                    i += 1
            else:
                result.append(tokens[i])
                i += 1
        
        return result

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
        
        # Paso 2: Expandir clases de caracteres
        expanded_tokens = self.expand_character_classes(tokens)
        steps.append(f"Clases expandidas: {expanded_tokens}")
        
        # Paso 3: Expandir + y ? a forma atómica
        atomic_tokens = self.expand_plus_and_question(expanded_tokens)
        steps.append(f"Forma atómica: {atomic_tokens}")
        
        # Paso 4: Agregar concatenación explícita
        tokens_with_concat = self.add_concatenation(atomic_tokens)
        steps.append(f"Con concatenación: {tokens_with_concat}")
        
        # Paso 5: Aplicar Shunting Yard
        output = []
        stack = []
        steps.append("Iniciando Shunting Yard:")
        
        for i, token in enumerate(tokens_with_concat):
            step_info = f"  Paso {i+1}: '{token}'"
            
            if self.is_literal(token):
                # PROCESAR ESCAPES: Si es un carácter escapado, solo agregar el carácter
                if len(token) == 2 and token[0] == '\\':
                    # literal_char = token[1]  # Solo el carácter sin el backslash
                    output.append(token)
                    step_info += f" -> Escape '{token}' -> preservado en la salida: {output}"
                else:
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
        
        postfix_tokens = output
        postfix_string = ''.join(output)
        steps.append(f"Postfija final (tokens): {postfix_tokens}")
        steps.append(f"Postfija final (string): {postfix_string}")
    
        return postfix_tokens, steps
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
                postfix = ''.join(postfix)
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
    print("=== ALGORITMO SHUNTING YARD CON SOPORTE PARA RANGOS ===")
    print("Convierte expresiones regulares a forma atómica postfija.\n")
    
    converter = ShuntingYard()
    
    # Casos de prueba incluyendo rangos
    test_expressions = [
        "[ae03]",       # Clase simple
        "[a-z]",        # Rango de letras minúsculas
        "[A-Z]",        # Rango de letras mayúsculas
        "[0-9]",        # Rango de dígitos
        "[a-zA-Z]",     # Múltiples rangos
        "[a-z0-9]",     # Rango + rango
        "[abc0-9]",     # Literales + rango
        "[a-c-f]",      # Rango + guión literal + literal
        "[-abc]",       # Guión literal al principio
        "[abc-]",       # Guión literal al final
        "[a-z]*",       # Rango con *
        "[0-9]+",       # Rango con +
        "a[b-d]e",      # Concatenación con rango
        "\[a-z\][0-9]",   # Dos rangos concatenados
    ]
    
    print("CASOS DE PRUEBA CON RANGOS:")
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
