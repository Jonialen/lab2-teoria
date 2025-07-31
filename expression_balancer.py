# expression_balancer.py (expression_balancer.py)

class ExpressionBalancer:
    """Valida si las expresiones tienen paréntesis, corchetes y llaves balanceados"""
    
    def __init__(self):
        self.opening_symbols = {'(', '[', '{'}
        self.closing_symbols = {')', ']', '}'}
        self.pairs = {'(': ')', '[': ']', '{': '}'}
    
    def is_balanced(self, expression):
        """
        Comprueba si la expresión tiene símbolos balanceados y devuelve el proceso paso a paso
        Returns: (is_balanced: bool, steps: list)
        """
        stack = []
        steps = []
        
        steps.append(f"Procesando expresión: {expression}")
        steps.append("Pila inicial: []")
        
        for i, char in enumerate(expression):
            if char in self.opening_symbols:
                stack.append(char)
                steps.append(f"Posición {i}: Se encontró apertura '{char}' -> Empujar a la pila: {stack}")
            
            elif char in self.closing_symbols:
                if not stack:
                    steps.append(f"Posición {i}: Se encontró cierre '{char}' pero la pila está vacía -> NO BALANCEADO")
                    return False, steps
                
                top = stack.pop()
                if self.pairs[top] == char:
                    steps.append(f"Posición {i}: Se encontró cierre '{char}' que coincide con apertura '{top}' -> Sacar de la pila: {stack}")
                else:
                    steps.append(f"Posición {i}: Se encontró cierre '{char}' no coincide con apertura '{top}' -> NO BALANCEADO")
                    return False, steps
        
        is_balanced = len(stack) == 0
        final_state = "BALANCEADO" if is_balanced else "NO BALANCEADO"
        steps.append(f"Pila final: {stack} -> {final_state}")
        
        return is_balanced, steps
    
    def process_file(self, filename):
        """Procesa un archivo con expresiones línea por línea"""
        results = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            print(f"Procesando archivo: {filename}")
            print("=" * 50)
            
            for line_num, line in enumerate(lines, 1):
                expression = line.strip()
                if not expression:
                    continue
                
                print(f"\nLínea {line_num}:")
                is_balanced, steps = self.is_balanced(expression)
                
                for step in steps:
                    print(f"  {step}")
                
                result_str = 'BALANCEADO' if is_balanced else 'NO BALANCEADO'
                print(f"  Resultado: {result_str}")
                print("-" * 40)
                results.append(f"{expression}: {result_str}")
        
        except FileNotFoundError:
            print(f"Error: Archivo '{filename}' no encontrado")
        except Exception as e:
            print(f"Error procesando archivo: {e}")
        
        return results


def main():
    """Función principal para procesar expresiones"""
    # Procesar expresiones
    balancer = ExpressionBalancer()
    balancer.process_file('expressions.txt')


if __name__ == "__main__":
    main()
