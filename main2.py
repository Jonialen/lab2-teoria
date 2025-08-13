# main2.py (main2.py)

import os
from shunting_yard import ShuntingYard
from ast_builder import ASTBuilder
from ast_visualizer import ASTVisualizer


class RegexASTProcessor:
    """Clase principal para procesar expresiones regulares y crear ASTs"""
    
    def __init__(self):
        self.shunting_yard = ShuntingYard()
        self.ast_builder = ASTBuilder()
        self.visualizer = ASTVisualizer()
    
    def process_expressions_from_file(self, filename):
        """Procesa todas las expresiones de un archivo y crea los ASTs"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                expressions = [line.strip() for line in file.readlines() if line.strip()]
            
            print(f"Procesando {len(expressions)} expresiones de {filename}")
            print("=" * 80)
            
            results = []
            
            for i, expression in enumerate(expressions, 1):
                print(f"\n{'='*20} EXPRESIÓN {i} {'='*20}")
                print(f"Expresión Original: {expression}")
                print("-" * 60)
                
                result = self.process_single_expression(expression, f"expr_{i}")
                results.append(result)
                
                print("\n" + "="*60)
            
            return results
            
        except FileNotFoundError:
            print(f"Error: Archivo '{filename}' no encontrado")
            return []
        except Exception as e:
            print(f"Error procesando archivo: {e}")
            return []
    
    def process_single_expression(self, expression, name):
        """Procesa una sola expresión: infijo -> postfijo -> AST -> visualización"""
        try:
            # Paso 1: Convertir de infijo a postfijo
            print("PASO 1: Convirtiendo infijo a postfijo usando Shunting Yard")
            postfix, shunting_steps = self.shunting_yard.infix_to_postfix(expression)
            
            print("Pasos de Shunting Yard:")
            for step in shunting_steps:
                print(f"  {step}")
            
            print(f"\nResultado postfijo: {postfix}")
            
            # Paso 2: Construir el AST a partir del postfijo
            print("\nPASO 2: Construyendo AST desde la expresión postfija")
            ast_root, ast_steps = self.ast_builder.build_ast(postfix)
            print("Pasos de construcción de AST:")
            for step in ast_steps:
                print(f"  {step}")
            
            # Paso 3: Imprimir la estructura del AST
            print("\nPASO 3: Estructura del AST")
            self.ast_builder.print_ast(ast_root)
            
            # Paso 4: Visualizar el AST
            print("\nPASO 4: Creando representación visual")
            dot = self.visualizer.visualize_ast(ast_root, f"{name}: {expression}")
            
            # Guardar la visualización
            filename = f"ast_{name}"
            success = self.visualizer.save_and_view(dot, filename, view=False)
            
            if success:
                print(f"Visualización del AST guardada como {filename}.png")
            
            return {
                'expression': expression,
                'postfix': postfix,
                'ast_root': ast_root,
                'success': True
            }
            
        except Exception as e:
            print(f"ERROR procesando la expresión '{expression}': {e}")
            return {
                'expression': expression,
                'error': str(e),
                'success': False
            }


def main():
    """Función principal"""
    print("=" * 80)
    print("LABORATORIO 3 - EJERCICIO 1")
    print("Conversión de Expresiones Regulares a AST")
    print("=" * 80)
    
    processor = RegexASTProcessor()
    
    # Definir el archivo de entrada
    input_file = "expressions.txt"
    
    # Procesar todas las expresiones
    results = processor.process_expressions_from_file(input_file)
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN DE RESULTADOS")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['success'])
    print(f"Expresiones procesadas exitosamente: {successful}/{len(results)}")
    
    for i, result in enumerate(results, 1):
        if result['success']:
            print(f"{i}. {result['expression']} -> {result['postfix']} Exito")
        else:
            print(f"{i}. {result['expression']} -> ERROR: {result['error']} Fallo")
    
    print(f"\nArchivos generados:")
    for i in range(1, len(results) + 1):
        if os.path.exists(f"ast_expr_{i}.png"):
            print(f"  - ast_expr_{i}.png")


if __name__ == "__main__":
    main()
