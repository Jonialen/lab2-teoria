# shunting_yard.py (shunting_yard.py)

from expression_balancer import ExpressionBalancer

class ShuntingYard:
    """
    Implementa el algoritmo de Shunting Yard para convertir expresiones regulares
    de notación infix a postfix.
    """

    def __init__(self):
        # Precedencia de operadores (mayor número = mayor precedencia)
        self.precedence = {
            '|': 1,  # alternancia (unión)
            '.': 2,  # concatenación (implícita)
            '?': 3,  # cero o uno
            '*': 3,  # cero o más
            '+': 3,  # uno o más
        }
        self.right_associative = {'?', '*', '+'}
        self.operators = set(self.precedence.keys())

    def preprocess_regex(self, regex):
        """
        Preprocesa la regex para convertir + y ? a su forma equivalente,
        y maneja caracteres escapados.
        """
        processed = []
        i = 0
        while i < len(regex):
            char = regex[i]
            # Manejo de caracteres escapados
            if char == '\\' and i + 1 < len(regex):
                processed.append('\\' + regex[i + 1])
                i += 2
                continue

            # Convertir + a equivalente: a+ = aa*
            if char == '+' and processed:
                operand, operand_length = self._extract_operand_with_length(processed)
                if operand:
                    # Remover el operando original
                    for _ in range(operand_length):
                        processed.pop()
                    # Agregar operando.operando*
                    processed.extend(list(operand))
                    processed.extend(list(operand))
                    processed.append('*')
                    i += 1
                    continue

            # Convertir ? a equivalente: a? = (ε|a)
            if char == '?' and processed:
                operand, operand_length = self._extract_operand_with_length(processed)
                if operand:
                    # Remover el operando original
                    for _ in range(operand_length):
                        processed.pop()
                    # Agregar (ε|operando)
                    processed.extend(['(', 'ε', '|'])
                    processed.extend(list(operand))
                    processed.append(')')
                    i += 1
                    continue

            processed.append(char)
            i += 1
        return ''.join(processed)

    def _extract_operand_with_length(self, processed):
        """
        Extrae el operando completo antes de un operador (+, ?) y devuelve
        tanto el operando como su longitud en la lista processed.
        """
        if not processed:
            return None, 0
        
        # Si el último carácter es un paréntesis de cierre, buscar el correspondiente de apertura
        if processed[-1] in ')]}':
            operand, start_pos = self._extract_balanced_with_position(processed)
            if operand and start_pos is not None:
                return operand, len(processed) - start_pos
            else:
                return processed[-1], 1
        
        # Si es un carácter escapado
        if len(processed) >= 2 and processed[-2] == '\\':
            return ''.join(processed[-2:]), 2
        
        # Si es un solo carácter
        return processed[-1], 1

    def _extract_balanced_with_position(self, processed):
        """
        Extrae una subexpresión balanceada desde el final de la lista
        y devuelve también la posición de inicio.
        """
        if not processed or processed[-1] not in ')]}':
            return None, None
            
        pairs = {')': '(', ']': '[', '}': '{'}
        closing = processed[-1]
        opening = pairs[closing]
        level = 1
        i = len(processed) - 2
        
        while i >= 0:
            if processed[i] == closing:
                level += 1
            elif processed[i] == opening:
                level -= 1
                if level == 0:
                    # Devuelve la subexpresión balanceada y la posición de inicio
                    return ''.join(processed[i:]), i
            i -= 1
        
        # Si no está balanceado, advertir y devolver solo el último carácter
        print("Advertencia: expresión no balanceada al extraer operando.")
        return processed[-1], len(processed) - 1

    def _extract_operand(self, processed):
        """
        Versión simplificada para compatibilidad (usa la nueva implementación).
        """
        operand, _ = self._extract_operand_with_length(processed)
        return operand

    def _extract_balanced(self, processed):
        """
        Versión simplificada para compatibilidad (usa la nueva implementación).
        """
        operand, _ = self._extract_balanced_with_position(processed)
        return operand

    def add_explicit_concatenation(self, regex):
        """
        Inserta el operador de concatenación '.' explícitamente donde sea necesario.
        """
        result = []
        for i in range(len(regex)):
            result.append(regex[i])
            if i < len(regex) - 1:
                curr, nxt = regex[i], regex[i + 1]
                # Condiciones para concatenar
                if (
                    (curr not in self.operators and curr not in '([{|' and
                     nxt not in self.operators and nxt not in ')]}|') or
                    (curr not in self.operators and curr not in '([{|' and nxt in '([') or
                    (curr in ')]}' and nxt not in self.operators and nxt not in ')]}|') or
                    (curr in ')]}' and nxt in '([') or
                    (curr in '*+?' and nxt not in self.operators and nxt not in ')]}|') or
                    (curr in '*+?' and nxt in '([')
                ):
                    result.append('.')
        return ''.join(result)

    def infix_to_postfix(self, infix):
        """
        Convierte una expresión infija a postfija usando el algoritmo de Shunting Yard.
        Devuelve la expresión postfija y los pasos realizados.
        """
        preprocessed = self.preprocess_regex(infix)
        processed_with_concat = self.add_explicit_concatenation(preprocessed)
        output_queue = []
        operator_stack = []
        steps = []
        steps.append(f"Original: {infix}")
        steps.append(f"Preprocesada: {preprocessed}")
        steps.append(f"Con concatenación: {processed_with_concat}")
        steps.append("Iniciando Shunting Yard:")

        for i, token in enumerate(processed_with_concat):
            step_info = f"Paso {i+1}: '{token}'"
            if token not in self.operators and token not in '()[]{}':
                output_queue.append(token)
                step_info += f" -> Salida: {output_queue}, Pila: {operator_stack}"
            elif token in self.operators:
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.operators and
                       (self.precedence[operator_stack[-1]] > self.precedence[token] or
                        (self.precedence[operator_stack[-1]] == self.precedence[token] and
                         token not in self.right_associative))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
                step_info += f" -> Pila: {operator_stack}, Salida: {output_queue}"
            elif token in '([{':
                operator_stack.append(token)
                step_info += f" -> Pila: {operator_stack}, Salida: {output_queue}"
            elif token in ')]}':
                pairs = {')': '(', ']': '[', '}': '{'}
                opening = pairs[token]
                while operator_stack and operator_stack[-1] != opening:
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == opening:
                    operator_stack.pop()
                step_info += f" -> Pila: {operator_stack}, Salida: {output_queue}"
            steps.append(step_info)

        while operator_stack:
            output_queue.append(operator_stack.pop())
        steps.append(f"Final: Salida: {output_queue}, Pila vacía")
        postfix = ''.join(output_queue)
        steps.append(f"Postfija: {postfix}")
        return postfix, steps

    def process_expressions(self, expressions):
        """
        Procesa una lista de expresiones, mostrando pasos y resultados.
        """
        results = []
        balancer = ExpressionBalancer()
        for idx, expression in enumerate(expressions, 1):
            print(f"\nExpresión {idx}: {expression}")
            print("-" * 50)
            is_balanced, balance_steps = balancer.is_balanced(expression)
            for step in balance_steps:
                print(f"  [Balanceo] {step}")
            if not is_balanced:
                print("  Resultado: NO BALANCEADA. Se omite conversión.")
                results.append(f"{expression} -> UNBALANCED, SKIPPED")
                continue
            print("  Balanceada. Aplicando Shunting Yard...")
            postfix, steps = self.infix_to_postfix(expression)
            for step in steps:
                print(f"  {step}")
            print(f"  Resultado final: {postfix}")
            results.append(f"{expression} -> {postfix}")
        return results

    def process_file(self, filename):
        """
        Procesa expresiones desde un archivo.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
            return self.process_expressions(lines)
        except FileNotFoundError:
            print(f"Archivo '{filename}' no encontrado.")
            return []
        except Exception as e:
            print(f"Error procesando archivo: {e}")
            return []

def main():
    print("=== ALGORITMO SHUNTING YARD ===")
    print("Convierte expresiones regulares infijas a postfijas.\n")
    converter = ShuntingYard()
    converter.process_file('expressions.txt')


if __name__ == "__main__":
    main()