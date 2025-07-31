# main.py (main.py)

import sys

# Importar nuestras clases personalizadas
from expression_balancer import ExpressionBalancer
from shunting_yard import ShuntingYard


def print_header(title):
    """Imprimir encabezado formateado"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_exercise_2():
    """Ejecutar Ejercicio 2 - Balanceador de Expresiones"""
    print_header("EJERCICIO 2: BALANCEADOR DE EXPRESIONES")
    
    filename = 'expressions.txt'

    balancer = ExpressionBalancer()
    return balancer.process_file(filename)


def run_exercise_3():
    """Ejecutar Ejercicio 3 - Algoritmo Shunting Yard"""
    print_header("EJERCICIO 3: ALGORITMO SHUNTING YARD")
    
    filename = 'expressions.txt'

    converter = ShuntingYard()
    return converter.process_file(filename)


def main():
    """Función principal para ejecutar ambos ejercicios"""
    
    all_results = []
    
    if len(sys.argv) > 1:
        exercise = sys.argv[1].lower()
        
        if exercise == "2" or exercise == "balancer":
            results_2 = run_exercise_2()
            all_results.extend(results_2)
        elif exercise == "3" or exercise == "shunting":
            results_3 = run_exercise_3()
            all_results.extend(results_3)
        else:
            print(f"Ejercicio desconocido: {exercise}")
    else:
        # Ejecutar ambos ejercicios
        results_2 = run_exercise_2()
        all_results.extend(["--- Resultados del Balanceador de Expresiones ---"])
        all_results.extend(results_2)
        
        input("\nPresione Enter para continuar al Ejercicio 3...")
        
        results_3 = run_exercise_3()
        all_results.extend(["\n--- Resultados de Shunting Yard ---"])
        all_results.extend(results_3)
    
    # Escribir resultados en output.txt
    with open('output.txt', 'w', encoding='utf-8') as f:
        for result in all_results:
            f.write(result + '\n')
            
    print("\n" + "=" * 60)
    print("EJECUCIÓN COMPLETADA")
    print("Los resultados resumidos han sido guardados en 'output.txt'")
    print("=" * 60)


if __name__ == "__main__":
    main()