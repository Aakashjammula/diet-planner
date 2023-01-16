from ortools.linear_solver import pywraplp
import os
import tempfile
import webbrowser
import time
from prettytable import PrettyTable
def dietplan():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver('diet_optimization', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    # Detailed instructions on how to use the program
    print()
    print("+------------------------------------------------------------------------------------------+")
    print("|                           Welcome to the diet planner!                                   |\n"
          "|------------------------------------------------------------------------------------      |\n"
        "| Please enter the cost, protein content, calorie content, and weight for each food item.  |\n"
        "| Also, enter the minimum and maximum daily requirements for protein and calories.         |\n"
        "| You can also enter a list of food items that you do not want to include in your diet plan|\n"
        "| We will then generate an optimal diet plan for you based on the given constraints.       |")
    print("+------------------------------------------------------------------------------------------+")
    # Get user to decide how many food they want to choose 
    print("Enter the number of foods you want to choose:")
    number_of_foods = int(input())
    # initialise cost and nutrient list
    costs = []
    protein = []
    calories = []
    weights = []
    excluded_foods = []
    for i in range(number_of_foods):
        # Get user input for the food cost, protein content, calorie content, and weight
        cost = float(input(f'Enter the cost of food{i+1}: '))
        if cost < 0:
            print(f'Invalid cost of food{i+1}. Cost should be greater than zero.')
            return
        costs.append(cost)
        protein_content = float(input(f'Enter the protein content of food{i+1}(per 100g): '))
        if protein_content < 0:
            print(f'Invalid protein content of food{i+1}. Protein content should be greater than zero.')
            return
        protein.append(protein_content)
        calorie_content = float(input(f'Enter the calorie content of food{i+1} (per 100g): '))
        if calorie_content < 0:
            print(f'Invalid calorie content of food{i+1}. Calorie content should be greater than zero.')
            return
        calories.append(calorie_content)
        weight = float(input(f'Enter the weight of food{i+1} (in g): '))
        if weight <= 0:
            print(f'Invalid weight of food{i+1}. weight should be greater than zero.')
            return
        weights.append(weight)
    # Get user input for the minimum and maximum daily requirements for protein and calories
    protein_min_req = float(input('Enter the minimum daily requirement of protein (in g): '))
    if protein_min_req <= 0:
        print(f'Invalid minimum daily requirement of protein. It shouldbe greater than zero.')
        return
    protein_max_req = float(input('Enter the maximum daily requirement of protein (in g): '))
    if protein_max_req < protein_min_req:
        print(f'Invalid maximum daily requirement of protein. It should be greater than or equal to the minimum requirement.')
        return
    # continue
    calories_min_req = float(input('Enter the minimum daily requirement of calories (in kcal): '))
    if calories_min_req <= 0:
        print(f'Invalid minimum daily requirement of calories. It should be greater than zero.')
        return
    calories_max_req = float(input('Enter the maximum daily requirement of calories (in kcal): '))
    if calories_max_req < calories_min_req:
        print(f'Invalid maximum daily requirement of calories. It should be greater than or equal to the minimum requirement.')
        return
    # Ask the user if they want to exclude any food items
    print("Do you want to exclude any food items? (yes/no)")
    exclude_food = input()
    if exclude_food == "yes":
        # Get user input for the list of foods to exclude
        print("Enter a list of food items that you do not want to include in your diet plan (separated by commas):")
        excluded_foods = [int(x) for x in input().split(',')]
    else:
        excluded_foods = []
    # Define the variables
    variables = []
    for i in range(number_of_foods):
        if i+1 not in excluded_foods:
            variables.append(solver.NumVar(0, solver.infinity(), f'food{i+1}'))
    # Define the objective function
    objective = solver.Objective()
    for i in range(number_of_foods):
        if i+1 not in excluded_foods:
            objective.SetCoefficient(variables[i], costs[i])
    objective.SetMinimization()
    # Define the constraints
    # Protein constraint
    protein_constraint = solver.Constraint(protein_min_req, protein_max_req)
    for i in range(number_of_foods):
        if i+1 not in excluded_foods:
            protein_constraint.SetCoefficient(variables[i], protein[i]*weights[i]/100)
    # Calories constraint
    calories_constraint = solver.Constraint(calories_min_req, calories_max_req)
    for i in range(number_of_foods):
        if i+1 not in excluded_foods:
            calories_constraint.SetCoefficient(variables[i], calories[i]*weights[i]/100)
    # Solve the problem
    status = solver.Solve()
    # Print the status of the solution
    print("Status:",(status))

    # Print the solution
    if status == pywraplp.Solver.OPTIMAL:
        table = PrettyTable()
        table.field_names = ["Food Item", "Amount (g)", "Cost", "Protein (g)", "Calories (kcal)", "Weight (g)"]
        total_protein = 0
        total_calories = 0
        total_cost = 0
        for i in range(number_of_foods):
            if i+1 not in excluded_foods:
                if variables[i].solution_value() > 0:
                    total_protein += protein[i]*weights[i]*variables[i].solution_value()/100
                    total_calories += calories[i]*weights[i]*variables[i].solution_value()/100
                    total_cost += costs[i]*variables[i].solution_value()
        for i in range(number_of_foods):
            if i+1 not in excluded_foods:
                if variables[i].solution_value() > 0:
                    table.add_row([f'food{i+1}', f'{variables[i].solution_value():.4f}', f'${costs[i]*variables[i].solution_value():.4f}', f'{protein[i]*weights[i]*variables[i].solution_value()/100:.4f}', f'{calories[i]*weights[i]*variables[i].solution_value()/100:.4f}', f'{weights[i]*variables[i].solution_value():.4f}'])
        print(table)
        print("\nDo you want to save or print your diet plan? (Enter 'save' or 'print')")
        user_choice = input()
        if user_choice == 'save':
            try:
                import pyperclip
            except ImportError:
                print("Please install the pyperclip library by running '!pip install pyperclip' in your command line.")
                return
            diet_plan = str(table) + '\n' + f'Total Cost: ${total_cost:.2f}\n' + f'Total Protein: {total_protein:.2f}g\n'+ f'Total Calories: {total_calories:.2f}kcal\n'
            pyperclip.copy(diet_plan)
            print("Diet plan saved to clipboard!")
        elif user_choice == 'print':
            # code to print the diet plan
            #create the html file containing the diet plan
            html = f'''<html>
            <head>
            <style>
            table, th, td {{
                border: 1px solid black;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 5px;
            }}
            </style>
            </head>
            <body>
            <h1>Diet Plan</h1>
            <table>
            <tr>
            <th>Food Item</th>
            <th>Amount (g)</th>
            <th>Cost</th>
            <th>Protein (g)</th>
            <th>Calories (kcal)</th>
            <th>Weight (g)</th>
            </tr>
            {table.get_html_string()}
            </table>
            <p>Total Cost: ${total_cost:.2f}</p>
            <p>Total Protein: {total_protein:.2f}g</p>
            </body>
            </html>'''
            #create a temporary file to store the html file
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(html.encode('utf-8'))
            temp_file.close()
            #open the html file in the default browser
            webbrowser.open(temp_file.name)
            # and click control+p to print the file
            time.sleep(10)
            import pyautogui
            pyautogui.hotkey('ctrl', 'p')

            
            #wait for the user to print the file
            time.sleep(6)
            print("Diet plan printed!")
            #delete the temporary file
            os.remove(temp_file.name)

        else:
            print("Invalid choice")
    else:
        print('The problem does not have an optimal solution. Please check your inputs or make sure that your diet plan is feasible with the given inputs.')

if __name__ == '__main__':
    dietplan()