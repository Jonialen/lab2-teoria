# expression_balancer.py (expression_balancer.py)

class ExpressionBalancer:
    """
    Verifica el balance de paréntesis en expresiones regulares.
    """
    
    def __init__(self):
        self.steps = []
    
    def is_balanced(self, expression):
        """
        Verifica si los paréntesis están balanceados en la expresión.
        Retorna (is_balanced: bool, steps: list)
        """
        self.steps = []
        stack = []
        position = 0
        
        for i, char in enumerate(expression):
            # Saltar caracteres escapados
            if i > 0 and expression[i-1] == '\\':
                continue
                
            if char == '(':
                stack.append(i)
                self.steps.append(f"Posición {i}: '(' - nivel {len(stack)}")
                
            elif char == ')':
                if not stack:
                    self.steps.append(f"Posición {i}: ')' sin '(' correspondiente")
                    return False, self.steps
                
                open_pos = stack.pop()
                self.steps.append(f"Posición {i}: ')' - cierra '(' en posición {open_pos}")
        
        if stack:
            self.steps.append(f"'(' sin cerrar en posiciones: {stack}")
            return False, self.steps
        
        self.steps.append("Expresión balanceada correctamente")
        return True, self.steps
    
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
