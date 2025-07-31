# main2.py (main2.py)

import os
from shunting_yard import ShuntingYard
from ast_builder import ASTBuilder
from ast_visualizer import ASTVisualizer


class RegexASTProcessor:
    """Main class for processing regular expressions and creating ASTs"""
    
    def __init__(self):
        self.shunting_yard = ShuntingYard()
        self.ast_builder = ASTBuilder()
        self.visualizer = ASTVisualizer()
    
    def process_expressions_from_file(self, filename):
        """Process all expressions from file and create ASTs"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                expressions = [line.strip() for line in file.readlines() if line.strip()]
            
            print(f"Processing {len(expressions)} expressions from {filename}")
            print("=" * 80)
            
            results = []
            
            for i, expression in enumerate(expressions, 1):
                print(f"\n{'='*20} EXPRESSION {i} {'='*20}")
                print(f"Original Expression: {expression}")
                print("-" * 60)
                
                result = self.process_single_expression(expression, f"expr_{i}")
                results.append(result)
                
                print("\n" + "="*60)
            
            return results
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            return []
        except Exception as e:
            print(f"Error processing file: {e}")
            return []
    
    def process_single_expression(self, expression, name):
        """Process a single expression: infix -> postfix -> AST -> visualization"""
        try:
            # Step 1: Convert infix to postfix
            print("STEP 1: Converting infix to postfix using Shunting Yard")
            postfix, shunting_steps = self.shunting_yard.infix_to_postfix(expression)
            
            print("Shunting Yard steps:")
            for step in shunting_steps:
                print(f"  {step}")
            
            print(f"\nPostfix result: {postfix}")
            
            # Step 2: Build AST from postfix
            print("\nSTEP 2: Building AST from postfix expression")
            ast_root, ast_steps = self.ast_builder.build_ast(postfix)
            
            print("AST construction steps:")
            for step in ast_steps:
                print(f"  {step}")
            
            # Step 3: Print AST structure
            print("\nSTEP 3: AST Structure")
            self.ast_builder.print_ast(ast_root)
            
            # Step 4: Visualize AST
            print("\nSTEP 4: Creating visual representation")
            dot = self.visualizer.visualize_ast(ast_root, f"{name}: {expression}")
            
            # Save the visualization
            filename = f"ast_{name}"
            success = self.visualizer.save_and_view(dot, filename, view=False)
            
            if success:
                print(f"AST visualization saved as {filename}.png")
            
            return {
                'expression': expression,
                'postfix': postfix,
                'ast_root': ast_root,
                'success': True
            }
            
        except Exception as e:
            print(f"ERROR processing expression '{expression}': {e}")
            return {
                'expression': expression,
                'error': str(e),
                'success': False
            }
    
    def create_test_file(self):
        """Create test file with the required expressions"""
        expressions = [
            "(a*|b*)+",
            "((ε|a)|b*)*", 
            "(a|b)*abb(a|b)*",
            "0?(1?)?0*"
        ]
        
        filename = "lab3_expressions.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            for expr in expressions:
                file.write(expr + '\n')
        
        print(f"Test file '{filename}' created with required expressions")
        return filename


def main():
    """Main function"""
    print("=" * 80)
    print("LABORATORIO 3 - EJERCICIO 1")
    print("Conversión de Expresiones Regulares a AST")
    print("=" * 80)
    
    processor = RegexASTProcessor()
    
    # Create test file with required expressions
    test_file = processor.create_test_file()
    
    # Process all expressions
    results = processor.process_expressions_from_file(test_file)
    
    # Summary
    print("\n" + "=" * 80)
    print("RESUMEN DE RESULTADOS")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['success'])
    print(f"Expresiones procesadas exitosamente: {successful}/{len(results)}")
    
    for i, result in enumerate(results, 1):
        if result['success']:
            print(f"{i}. {result['expression']} -> {result['postfix']} ✓")
        else:
            print(f"{i}. {result['expression']} -> ERROR: {result['error']} ✗")
    
    print(f"\nArchivos generados:")
    for i in range(1, len(results) + 1):
        if os.path.exists(f"ast_expr_{i}.png"):
            print(f"  - ast_expr_{i}.png")


if __name__ == "__main__":
    main()
