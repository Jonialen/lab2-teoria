# shunting_yard.py (shunting_yard.py)

class ShuntingYard:
    """
    Implementa el algoritmo de Shunting Yard para convertir expresiones regulares
    de notación infix a postfix
    """
    
    def __init__(self):
        # Operator precedence (higher number = higher precedence)
        self.precedence = {
            '|': 1,  # alternation (union)
            '.': 2,  # concatenation (implicit)
            '?': 3,  # zero or one
            '*': 3,  # zero or more
            '+': 3,  # one or more
        }
        
        self.right_associative = {'?', '*', '+'}
        self.operators = set(self.precedence.keys())
    
    def preprocess_regex(self, regex):
        """
        Preprocess regex to handle escape characters and convert + and ? operators
        """
        processed = []
        i = 0
        
        while i < len(regex):
            char = regex[i]
            
            # Handle escape characters
            if char == '\\' and i + 1 < len(regex):
                processed.append(regex[i + 1])  # Add escaped character
                i += 2
                continue
            
            # Convert + to equivalent form: a+ = aa*
            if char == '+' and processed:
                last_char = processed[-1]
                if last_char not in self.operators and last_char not in '()[]{}':
                    processed.append(last_char)  # Duplicate last character
                    processed.append('*')  # Add Kleene star
                    i += 1
                    continue
            
            # Convert ? to equivalent form: a? = (ε|a)
            if char == '?' and processed:
                last_char = processed.pop()  # Remove last character
                processed.extend(['(', 'ε', '|', last_char, ')'])
                i += 1
                continue
            
            processed.append(char)
            i += 1
        
        return ''.join(processed)
    
    def add_explicit_concatenation(self, regex):
        """Add explicit concatenation operators"""
        result = []
        
        for i in range(len(regex)):
            result.append(regex[i])
            
            if i < len(regex) - 1:
                current = regex[i]
                next_char = regex[i + 1]
                
                # Add concatenation between:
                # - character and character
                # - character and (
                # - ) and character
                # - ) and (
                # - character and [
                # - ] and character
                
                needs_concat = (
                    (current not in self.operators and current not in '()[]{}' and 
                     next_char not in self.operators and next_char not in '()[]{}') or
                    (current not in self.operators and current not in '()[]{}' and next_char == '(') or
                    (current == ')' and next_char not in self.operators and next_char not in '()[]{}') or
                    (current == ')' and next_char == '(') or
                    (current not in self.operators and current not in '()[]{}' and next_char == '[') or
                    (current == ']' and next_char not in self.operators and next_char not in '()[]{}') or
                    (current == ']' and next_char == '(') or
                    (current == '*' and next_char not in self.operators and next_char not in '()[]{}|') or
                    (current == '*' and next_char == '(')
                )
                
                if needs_concat:
                    result.append('.')
        
        return ''.join(result)
    
    def infix_to_postfix(self, infix):
        """
        Convert infix expression to postfix using Shunting Yard algorithm
        Returns: (postfix_expression, steps)
        """
        # Preprocess the regex
        preprocessed = self.preprocess_regex(infix)
        processed_with_concat = self.add_explicit_concatenation(preprocessed)
        
        output_queue = []
        operator_stack = []
        steps = []
        
        steps.append(f"Original expression: {infix}")
        steps.append(f"After preprocessing: {preprocessed}")
        steps.append(f"After adding concatenation: {processed_with_concat}")
        steps.append("Starting Shunting Yard algorithm:")
        steps.append("Initial state - Output: [], Stack: []")
        
        for i, token in enumerate(processed_with_concat):
            step_info = f"Step {i+1}: Processing '{token}'"
            
            # If token is operand (character)
            if token not in self.operators and token not in '()[]{}':
                output_queue.append(token)
                step_info += f" -> Add to output: {output_queue}, Stack: {operator_stack}"
            
            # If token is operator
            elif token in self.operators:
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.operators and
                       (self.precedence[operator_stack[-1]] > self.precedence[token] or
                        (self.precedence[operator_stack[-1]] == self.precedence[token] and 
                         token not in self.right_associative))):
                    
                    output_queue.append(operator_stack.pop())
                
                operator_stack.append(token)
                step_info += f" -> Pop higher precedence, push operator: Output: {output_queue}, Stack: {operator_stack}"
            
            # If token is left parenthesis
            elif token in '([{':
                operator_stack.append(token)
                step_info += f" -> Push opening bracket: Output: {output_queue}, Stack: {operator_stack}"
            
            # If token is right parenthesis
            elif token in ')]}':
                # Map closing brackets to opening brackets
                bracket_pairs = {')': '(', ']': '[', '}': '{'}
                opening = bracket_pairs[token]
                while operator_stack and operator_stack[-1] != opening:
                    output_queue.append(operator_stack.pop())
                
                if operator_stack:
                    operator_stack.pop()  # Remove opening bracket
                
                step_info += f" -> Pop until opening bracket: Output: {output_queue}, Stack: {operator_stack}"
            
            steps.append(step_info)
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        steps.append(f"Final step: Pop remaining operators: Output: {output_queue}, Stack: {operator_stack}")
        
        postfix = ''.join(output_queue)
        steps.append(f"Final postfix expression: {postfix}")
        
        return postfix, steps
    
    def process_file(self, filename):
        """Process expressions from file"""
        results = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            print(f"Processing file: {filename}")
            print("=" * 70)
            
            for line_num, line in enumerate(lines, 1):
                expression = line.strip()
                if not expression:
                    continue
                
                print(f"\nExpression {line_num}: {expression}")
                print("-" * 50)
                
                postfix, steps = self.infix_to_postfix(expression)
                
                for step in steps:
                    print(f"  {step}")
                
                print(f"\nFinal Result: {postfix}")
                print("=" * 70)
                results.append(f"{expression} -> {postfix}")
        
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error processing file: {e}")
        
        return results


def create_regex_test_file():
    """Create test file with regex expressions from Exercise 1"""
    expressions = [
        "(a|t)c",
        "(a|b)*",
        "(a*|b*)*",
        "((ε|a)|b*)*",
        "(a|b)*abb(a|b)*",
        "0?(1?)?0*",
        "if\\([ae]+\\)\\{[ei]+\\}(\\n(else\\{[jl]+\\}))?",
        "[ae03]+@[ae03]+.(com|net|org)(.(gt|cr|co))?"
    ]
    
    with open('regex_expressions.txt', 'w', encoding='utf-8') as file:
        for expr in expressions:
            file.write(expr + '\n')
    
    print("Test file 'regex_expressions.txt' created successfully!")


def main():
    print("=== SHUNTING YARD ALGORITHM ===")
    print("\nBrief explanation:")
    print("The Shunting Yard algorithm converts infix notation to postfix notation.")
    print("It uses a stack to hold operators and outputs operands directly.")
    print("Operators are popped based on precedence and associativity rules.")
    print("Parentheses are handled by pushing opening ones and popping until")
    print("the matching closing one is found.\n")
    
    # Create test file
    create_regex_test_file()
    
    # Process expressions
    converter = ShuntingYard()
    converter.process_file('regex_expressions.txt')


if __name__ == "__main__":
    main()
