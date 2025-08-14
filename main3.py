# main3.py (main3.py)

import os
from shunting_yard import ShuntingYard
from ast_builder import ASTBuilder
from ast_visualizer import ASTVisualizer
from thompson import ThompsonConstructor
from nfa_visualizer import NFAVisualizer
from nfa_simulator import NFASimulator


class RegexProcessor:
    """Clase principal para procesar expresiones regulares completas"""
    
    def __init__(self):
        self.shunting_yard = ShuntingYard()
        self.ast_builder = ASTBuilder()
        self.ast_visualizer = ASTVisualizer()
        self.thompson = ThompsonConstructor()
        self.nfa_visualizer = NFAVisualizer()
    
    def process_expressions_from_file(self, filename):
        """Procesa todas las expresiones de un archivo"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                expressions = [line.strip() for line in file.readlines() if line.strip()]
            
            print(f"Procesando {len(expressions)} expresiones de {filename}")
            print("=" * 80)
            
            # Cadenas de prueba para cada expresión
            test_strings = [
                ["a", "b", "aa", "bb", "ab", "ba", "aab", "bba", ""],
                ["", "a", "b", "ab", "ba", "bb", "aab", "bba"],
                ["abb", "aabb", "babb", "abba", "aabba", "ab", "bb", ""],
                ["", "0", "1", "01", "10", "00", "000", "010"]
            ]
            
            results = []
            
            for i, expression in enumerate(expressions, 1):
                print(f"\n{'='*25} EXPRESIÓN {i} {'='*25}")
                print(f"Expresión Original: {expression}")
                print("-" * 70)
                
                result = self.process_complete_expression(
                    expression, f"expr_{i}", test_strings[min(i-1, len(test_strings)-1)]
                )
                results.append(result)
                
                print("\n" + "="*70)
            
            return results
            
        except FileNotFoundError:
            print(f"Error: Archivo '{filename}' no encontrado")
            return []
        except Exception as e:
            print(f"Error procesando archivo: {e}")
            return []
    
    def process_complete_expression(self, expression, name, test_strings):
        """Procesa completamente una expresión: infijo -> postfijo -> AST -> AFN -> simulación"""
        try:
            # Paso 1: Convertir a postfijo
            print("PASO 1: Convirtiendo infijo a postfijo (Shunting Yard)")
            postfix, _ = self.shunting_yard.infix_to_postfix(expression)
            print(f"Resultado postfijo: {postfix}")
            
            # Paso 2: Construir AST
            print("\nPASO 2: Construyendo AST")
            ast_root, _ = self.ast_builder.build_ast(postfix)
            print("AST construido exitosamente")
            
            # Paso 3: Generar AFN con Thompson
            print("\nPASO 3: Generando AFN (Algoritmo de Thompson)")
            nfa = self.thompson.construct_nfa(ast_root)
            nfa_info = nfa.get_states_info()
            print(f"AFN generado:")
            print(f"  Estados: {nfa_info['total_states']}")
            print(f"  Estado inicial: q{nfa_info['initial_state']}")
            print(f"  Estados finales: {[f'q{s}' for s in nfa_info['final_states']]}")
            print(f"  Alfabeto: {nfa_info['alphabet']}")
            
            # Paso 4: Visualizar AST y AFN
            print("\nPASO 4: Creando visualizaciones")
            
            # Visualizar AST
            ast_dot = self.ast_visualizer.visualize_ast(ast_root, f"{name}: {expression}")
            ast_success = self.ast_visualizer.save_and_view(ast_dot, f"ast_{name}", view=False)
            
            # Visualizar AFN
            nfa_dot = self.nfa_visualizer.visualize_nfa(nfa, f"{name}: {expression}")
            nfa_success = self.nfa_visualizer.save_and_view(nfa_dot, f"nfa_{name}", view=False)
            
            if ast_success:
                print(f"AST guardado como ast_{name}.png")
            if nfa_success:
                print(f"AFN guardado como nfa_{name}.png")
            
            # Paso 5: Simular AFN
            print(f"\nPASO 5: Simulando AFN con cadenas de prueba")
            simulator = NFASimulator(nfa)
            simulation_results = []
            
            for test_string in test_strings[:5]:  # Limitar a 5 cadenas por expresión
                print(f"\n--- Probando cadena: '{test_string}' ---")
                accepted, steps = simulator.simulate(test_string)
                
                # Mostrar solo los pasos más importantes
                print(f"Resultado: {'ACEPTA' if accepted else 'RECHAZA'}")
                simulation_results.append((test_string, accepted))
            
            # Resumen de simulaciones
            print(f"\nResumen de simulaciones:")
            for test_str, accepted in simulation_results:
                result = "✓" if accepted else "✗"
                print(f"  '{test_str}' -> {result}")
            
            return {
                'expression': expression,
                'postfix': postfix,
                'ast_root': ast_root,
                'nfa': nfa,
                'simulation_results': simulation_results,
                'success': True
            }
            
        except Exception as e:
            print(f"ERROR procesando '{expression}': {e}")
            import traceback
            traceback.print_exc()
            return {
                'expression': expression,
                'error': str(e),
                'success': False
            }


def main():
    """Función principal"""
    print("=" * 80)
    print("LABORATORIO - PROCESAMIENTO COMPLETO DE EXPRESIONES REGULARES")
    print("Shunting Yard -> AST -> Thompson -> AFN -> Simulación")
    print("=" * 80)
    
    processor = RegexProcessor()
    
    # Archivo de entrada
    input_file = "expressions.txt"
    
    # Procesar todas las expresiones
    results = processor.process_expressions_from_file(input_file)
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DE RESULTADOS")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['success'])
    print(f"Expresiones procesadas exitosamente: {successful}/{len(results)}")
    
    print(f"\nArchivos generados:")
    for i in range(1, len(results) + 1):
        if os.path.exists(f"ast_expr_{i}.png"):
            print(f"  - ast_expr_{i}.png (AST)")
        if os.path.exists(f"nfa_expr_{i}.png"):
            print(f"  - nfa_expr_{i}.png (AFN)")
    
    # Mostrar resultados de simulación
    print(f"\nResultados de simulaciones:")
    for i, result in enumerate(results, 1):
        if result['success'] and 'simulation_results' in result:
            print(f"\nExpresión {i}: {result['expression']}")
            for test_str, accepted in result['simulation_results']:
                symbol = "✓" if accepted else "✗"
                print(f"  '{test_str}' -> {symbol}")


if __name__ == "__main__":
    main()
