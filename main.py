# main.py (main.py)

import sys

# Import our custom classes
from expression_balancer import ExpressionBalancer, create_test_file
from shunting_yard import ShuntingYard, create_regex_test_file


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_exercise_2():
    """Execute Exercise 2 - Expression Balancer"""
    print_header("EXERCISE 2: EXPRESSION BALANCER")
    
    # Ask for filename
    filename = input("Enter the filename for the expression balancer (or press Enter for default): ").strip()
    
    if not filename:
        # Create test file and run balancer
        create_test_file()
        filename = 'expressions.txt'

    balancer = ExpressionBalancer()
    return balancer.process_file(filename)


def run_exercise_3():
    """Execute Exercise 3 - Shunting Yard Algorithm"""
    print_header("EXERCISE 3: SHUNTING YARD ALGORITHM")
    
    # Ask for filename
    filename = input("Enter the filename for the shunting yard (or press Enter for default): ").strip()

    if not filename:
        # Create test file and run converter
        create_regex_test_file()
        filename = 'regex_expressions.txt'

    converter = ShuntingYard()
    return converter.process_file(filename)


def main():
    """Main function to run both exercises"""
    
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
            print(f"Unknown exercise: {exercise}")
    else:
        # Run both exercises
        results_2 = run_exercise_2()
        all_results.extend(["--- Expression Balancer Results ---"])
        all_results.extend(results_2)
        
        input("\nPress Enter to continue to Exercise 3...")
        
        results_3 = run_exercise_3()
        all_results.extend(["\n--- Shunting Yard Results ---"])
        all_results.extend(results_3)
    
    # Write results to output.txt
    with open('output.txt', 'w', encoding='utf-8') as f:
        for result in all_results:
            f.write(result + '\n')
            
    print("\n" + "=" * 60)
    print("EXECUTION COMPLETED")
    print("Summarized results have been saved to 'output.txt'")
    print("=" * 60)

if __name__ == "__main__":
    main()