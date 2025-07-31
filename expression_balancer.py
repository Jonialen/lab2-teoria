# expression_balancer.py (expression_balancer.py)

class ExpressionBalancer:
    """Validates if expressions have balanced parentheses, brackets, and braces"""
    
    def __init__(self):
        self.opening_symbols = {'(', '[', '{'}
        self.closing_symbols = {')', ']', '}'}
        self.pairs = {'(': ')', '[': ']', '{': '}'}
    
    def is_balanced(self, expression):
        """
        Check if expression has balanced symbols and return step-by-step process
        Returns: (is_balanced: bool, steps: list)
        """
        stack = []
        steps = []
        
        steps.append(f"Processing expression: {expression}")
        steps.append("Initial stack: []")
        
        for i, char in enumerate(expression):
            if char in self.opening_symbols:
                stack.append(char)
                steps.append(f"Position {i}: Found opening '{char}' -> Push to stack: {stack}")
            
            elif char in self.closing_symbols:
                if not stack:
                    steps.append(f"Position {i}: Found closing '{char}' but stack is empty -> UNBALANCED")
                    return False, steps
                
                top = stack.pop()
                if self.pairs[top] == char:
                    steps.append(f"Position {i}: Found closing '{char}' matches opening '{top}' -> Pop from stack: {stack}")
                else:
                    steps.append(f"Position {i}: Found closing '{char}' doesn't match opening '{top}' -> UNBALANCED")
                    return False, steps
        
        is_balanced = len(stack) == 0
        final_state = "BALANCED" if is_balanced else "UNBALANCED"
        steps.append(f"Final stack: {stack} -> {final_state}")
        
        return is_balanced, steps
    
    def process_file(self, filename):
        """Process file with expressions line by line"""
        results = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            print(f"Processing file: {filename}")
            print("=" * 50)
            
            for line_num, line in enumerate(lines, 1):
                expression = line.strip()
                if not expression:
                    continue
                
                print(f"\nLine {line_num}:")
                is_balanced, steps = self.is_balanced(expression)
                
                for step in steps:
                    print(f"  {step}")
                
                result_str = 'BALANCED' if is_balanced else 'UNBALANCED'
                print(f"  Result: {result_str}")
                print("-" * 40)
                results.append(f"{expression}: {result_str}")
        
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error processing file: {e}")
        
        return results


def main():
    """Main function to process expressions"""
    # Process expressions
    balancer = ExpressionBalancer()
    balancer.process_file('expressions.txt')


if __name__ == "__main__":
    main()
