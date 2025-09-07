# main_project.py (main_project.py)

import os
import sys
from typing import List, Dict, Any

# Importar todos nuestros módulos
from shunting_yard import ShuntingYard
from ast_builder import ASTBuilder
from thompson import ThompsonConstructor
from subset_construction import SubsetConstruction
from dfa_minimizer import DFAMinimizer
from nfa_simulator import NFASimulator
from dfa_simulator import DFASimulator
from nfa_visualizer import NFAVisualizer
from dfa_visualizer import DFAVisualizer
from ast_visualizer import ASTVisualizer


class RegexProcessor:
    """Clase principal que integra todo el pipeline de procesamiento de expresiones regulares"""
    
    def __init__(self):
        # Inicializar todos los componentes
        self.shunting_yard = ShuntingYard()
        self.ast_builder = ASTBuilder()
        self.thompson = ThompsonConstructor()
        self.subset_constructor = SubsetConstruction()
        self.dfa_minimizer = DFAMinimizer()
        
        # Visualizadores
        self.ast_visualizer = ASTVisualizer()
        self.nfa_visualizer = NFAVisualizer()
        self.dfa_visualizer = DFAVisualizer()
        
        # Crear directorio de salida si no existe
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def process_file(self, filename: str, test_strings: List[str] = None) -> List[Dict[str, Any]]:
        """
        Procesa un archivo con expresiones regulares línea por línea
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                expressions = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Error: Archivo '{filename}' no encontrado")
            return []
        except Exception as e:
            print(f"Error leyendo archivo: {e}")
            return []
        
        if not expressions:
            print("No se encontraron expresiones válidas en el archivo")
            return []
        
        print(f"Procesando archivo: {filename}")
        print(f"Expresiones encontradas: {len(expressions)}")
        print("=" * 80)
        
        results = []
        
        # Cadenas de prueba por defecto si no se proporcionan
        if test_strings is None:
            test_strings = ["", "a", "b", "aa", "ab", "ba", "bb", "aaa", "aba", "bab"]
        
        # Procesar cada expresión
        for i, expression in enumerate(expressions, 1):
            print(f"\n{'='*20} EXPRESIÓN {i} {'='*20}")
            result = self.process_single_expression(expression, i, test_strings)
            results.append(result)
            print("=" * 60)
        
        # Generar resumen final
        self._generate_summary_report(results)
        
        return results
    
    def process_single_expression(self, expression: str, expr_num: int, test_strings: List[str]) -> Dict[str, Any]:
        """
        Procesa una sola expresión regular a través de todo el pipeline
        """
        result = {
            'expression': expression,
            'expr_num': expr_num,
            'success': False,
            'error': None,
            'postfix': None,
            'nfa_states': 0,
            'dfa_states': 0,
            'minimized_dfa_states': 0,
            'simulations': {}
        }
        
        try:
            print(f"Expresión: {expression}")
            
            # PASO 1: Conversión Infix a Postfix (Shunting Yard)
            print(f"\nPASO 1: Shunting Yard")
            postfix, shunting_steps = self.shunting_yard.infix_to_postfix(expression)
            
            if postfix is None:
                result['error'] = "Expresión no balanceada"
                print(f"Error: Expresión no balanceada")
                return result
            
            result['postfix'] = postfix
            print(f"Postfix: {postfix}", type(postfix))
            
            # PASO 2: Construcción de AST
            print(f"\nPASO 2: Construcción de AST")
            ast_root, ast_steps = self.ast_builder.build_ast(postfix)
            print(f"AST construido")
            
            # PASO 3: Construcción de AFN (Thompson)
            print(f"\nPASO 3: Construcción de AFN (Thompson)")
            nfa = self.thompson.construct_nfa(ast_root)
            result['nfa_states'] = len(nfa.states)
            print(f"AFN: {result['nfa_states']} estados, alfabeto: {sorted(nfa.alphabet)}")
            
            # PASO 4: Construcción de AFD (Subconjuntos)
            print(f"\nPASO 4: Construcción de AFD (Subconjuntos)")
            dfa, construction_steps = self.subset_constructor.construct_dfa(nfa)
            result['dfa_states'] = len(dfa.states)
            print(f"AFD: {result['dfa_states']} estados")
            
            # PASO 5: Minimización de AFD
            print(f"\nPASO 5: Minimización de AFD")
            minimized_dfa, minimization_steps = self.dfa_minimizer.minimize_dfa(dfa)
            result['minimized_dfa_states'] = len(minimized_dfa.states)
            print(f"AFD Minimizado: {result['minimized_dfa_states']} estados")
            
            # PASO 6: Crear visualizaciones
            print(f"\nPASO 6: Generando visualizaciones")
            self._create_visualizations(ast_root, nfa, dfa, minimized_dfa, expression, expr_num)
            
            # PASO 7: Simular autómatas
            print(f"\nPASO 7: Simulando con cadenas de prueba")
            simulations = self._run_simulations(nfa, dfa, minimized_dfa, test_strings)
            result['simulations'] = simulations
            
            # PASO 8: Mostrar resultados
            self._show_simulation_results(simulations, test_strings)
            
            result['success'] = True
            print(f"\nPROCESAMIENTO EXITOSO")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
        
        return result
    
    def _create_visualizations(self, ast_root, nfa, dfa, minimized_dfa, expression: str, expr_num: int):
        """Crea todas las visualizaciones para una expresión"""
        base_name = f"expr_{expr_num}"
        
        try:
            # AST
            ast_dot = self.ast_visualizer.visualize_ast(ast_root, f"{expr_num}: {expression}")
            ast_path = os.path.join(self.output_dir, f"{base_name}_ast")
            self.ast_visualizer.save_and_view(ast_dot, ast_path, view=False)
            
            # AFN
            nfa_dot = self.nfa_visualizer.visualize_nfa(nfa, f"{expr_num}: {expression}")
            nfa_path = os.path.join(self.output_dir, f"{base_name}_afn")
            self.nfa_visualizer.save_and_view(nfa_dot, nfa_path, view=False)
            
            # AFD
            dfa_dot = self.dfa_visualizer.visualize_dfa(dfa, f"{expr_num}: {expression}")
            dfa_path = os.path.join(self.output_dir, f"{base_name}_afd")
            self.dfa_visualizer.save_and_view(dfa_dot, dfa_path, view=False)
            
            # AFD Minimizado
            min_dfa_dot = self.dfa_visualizer.visualize_dfa(minimized_dfa, f"{expr_num}: {expression} (Min)")
            min_dfa_path = os.path.join(self.output_dir, f"{base_name}_afd_min")
            self.dfa_visualizer.save_and_view(min_dfa_dot, min_dfa_path, view=False)
            
            print(f"Visualizaciones guardadas en /{self.output_dir}/")
            
        except Exception as e:
            print(f"Error generando visualizaciones: {e}")
    
    def _run_simulations(self, nfa, dfa, minimized_dfa, test_strings: List[str]) -> Dict[str, List]:
        """Ejecuta simulaciones en todos los autómatas"""
        nfa_simulator = NFASimulator(nfa)
        dfa_simulator = DFASimulator(dfa)
        min_dfa_simulator = DFASimulator(minimized_dfa)
        
        simulations = {
            'nfa': [],
            'dfa': [],
            'minimized_dfa': []
        }
        
        for test_string in test_strings:
            # Simular AFN
            nfa_accepted, _ = nfa_simulator.simulate(test_string)
            simulations['nfa'].append((test_string, nfa_accepted))
            
            # Simular AFD
            dfa_accepted, _ = dfa_simulator.simulate(test_string)
            simulations['dfa'].append((test_string, dfa_accepted))
            
            # Simular AFD minimizado
            min_dfa_accepted, _ = min_dfa_simulator.simulate(test_string)
            simulations['minimized_dfa'].append((test_string, min_dfa_accepted))
        
        return simulations
    
    def _show_simulation_results(self, simulations: Dict[str, List], test_strings: List[str]):
        """Muestra los resultados de las simulaciones en formato tabla"""
        print(f"\nResultados de simulación:")
        print(f"  {'Cadena':<10} {'AFN':<5} {'AFD':<5} {'Min':<5} {'Equiv':<6}")
        print(f"  {'-'*10} {'-'*5} {'-'*5} {'-'*5} {'-'*6}")
        
        all_equivalent = True
        
        for i, test_string in enumerate(test_strings):
            nfa_result = simulations['nfa'][i][1]
            dfa_result = simulations['dfa'][i][1]
            min_dfa_result = simulations['minimized_dfa'][i][1]
            
            # Verificar equivalencia
            equivalent = nfa_result == dfa_result == min_dfa_result
            if not equivalent:
                all_equivalent = False
            
            # Símbolos para mostrar
            nfa_sym = "Si" if nfa_result else "No"
            dfa_sym = "Si" if dfa_result else "No"
            min_sym = "Si" if min_dfa_result else "No"
            equiv_sym = "Si" if equivalent else "No"
            
            display_string = f"'{test_string}'" if test_string else "'ε'"
            print(f"  {display_string:<10} {nfa_sym:<5} {dfa_sym:<5} {min_sym:<5} {equiv_sym:<6}")
        
        if all_equivalent:
            print(f"  Si Todos los autómatas son equivalentes")
        else:
            print(f"  Advertencia: Hay diferencias entre autómatas")
    
    def _generate_summary_report(self, results: List[Dict[str, Any]]):
        """Genera un reporte resumen de todo el procesamiento"""
        report_path = os.path.join(self.output_dir, "resumen_procesamiento.txt")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("REPORTE DE PROCESAMIENTO DE EXPRESIONES REGULARES\n")
                f.write("=" * 80 + "\n\n")
                
                successful = sum(1 for r in results if r['success'])
                f.write(f"Expresiones procesadas exitosamente: {successful}/{len(results)}\n\n")
                
                for result in results:
                    f.write(f"Expresión {result['expr_num']}: {result['expression']}\n")
                    if result['success']:
                        f.write(f"  Si Exitosa\n")
                        f.write(f"  Postfix: {result['postfix']}\n")
                        f.write(f"  AFN: {result['nfa_states']} estados\n")
                        f.write(f"  AFD: {result['dfa_states']} estados\n")
                        f.write(f"  AFD Min: {result['minimized_dfa_states']} estados\n")
                    else:
                        f.write(f"  No Error: {result['error']}\n")
                    f.write("\n")
                
                # Estadísticas generales
                if successful > 0:
                    avg_nfa_states = sum(r['nfa_states'] for r in results if r['success']) / successful
                    avg_dfa_states = sum(r['dfa_states'] for r in results if r['success']) / successful
                    avg_min_states = sum(r['minimized_dfa_states'] for r in results if r['success']) / successful
                    
                    f.write("ESTADÍSTICAS:\n")
                    f.write(f"  Promedio estados AFN: {avg_nfa_states:.1f}\n")
                    f.write(f"  Promedio estados AFD: {avg_dfa_states:.1f}\n")
                    f.write(f"  Promedio estados AFD Min: {avg_min_states:.1f}\n")
            
            print(f"\nReporte guardado en: {report_path}")
            
        except Exception as e:
            print(f"Error generando reporte: {e}")


def main():
    """Función principal del programa"""
    print("=" * 80)
    print("PROCESADOR DE EXPRESIONES REGULARES - PROYECTO COMPLETO")
    print("Pipeline: Infix → Postfix → AST → AFN → AFD → AFD Minimizado")
    print("=" * 80)
    
    # Configuración por defecto
    input_file = "expressions.txt"
    test_strings = ["", "a", "b", "aa", "ab", "ba", "bb", "aaa", "aba", "bab", "[a-z]0"]
    
    # Procesar argumentos de línea de comandos
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    # Verificar que el archivo existe
    if not os.path.exists(input_file):
        print(f"No Error: Archivo '{input_file}' no encontrado")
        print(f"Uso: python main_project.py [archivo_expresiones.txt]")
        return
    
    # Crear procesador y ejecutar
    processor = RegexProcessor()
    results = processor.process_file(input_file, test_strings)
    
    # Mostrar resumen final
    print("\n" + "=" * 80)
    print("RESUMEN FINAL")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['success'])
    print(f"Si Expresiones procesadas exitosamente: {successful}/{len(results)}")
    
    if successful > 0:
        print(f"Archivos generados en ./output/")
        print(f"   - {successful * 4} visualizaciones PNG (AST, AFN, AFD, AFD Min)")
        print(f"   - 1 reporte de resumen")
    
    print("\n¡PROCESAMIENTO COMPLETADO!")


if __name__ == "__main__":
    main()
