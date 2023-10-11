# Diet Planner



Diet Planner is a tool that helps users create a personalized diet plan that fits their dietary needs and constraints. 

It prompts the user to input information about various food items, such as their cost, protein content, calorie content, and weight, as well as their minimum and maximum daily requirements for protein and calories.

The code then uses advanced optimization techniques and the "pywraplp" library from Google's "ortools" package to generate an optimal diet plan that minimizes the cost of the diet while satisfying the user's dietary requirements and constraints.

The code then displays the optimal diet plan in a tabular format using the "prettytable" library, which makes it easy to read and understand. Additionally, the user can save the diet plan to a file in CSV format or open it in a web browser for easy viewing.
## Table of Contents

- [How to Install and Run the Project](#how-to-install-and-run-the-project)
- [How to Use the Project](#how-to-use-the-project)
- [License](#license)

## How to Install and Run the Project

1. Install the required packages using pip:

```shell
pip install pywraplp ortools prettytable pyperclip pyautogui tempfile 
```
2. Clone the repository or download the code
3. Run the code using Python: `python diet_planner.py`

## How to Use the Project

1. Run the code using Python: `python diet_planner.py`
2. The code will prompt the user to input information about various food items, such as their cost, protein content, calorie content, and weight, as well as their minimum and maximum daily requirements for protein and calories.
3. Follow the detailed instructions, input validation, and error handling to guide the user through the process.
4. Once the optimal diet plan is generated, it can be displayed in a tabular format using the "prettytable" library, which makes it easy to read and understand. Additionally, the user can save the diet plan to a file in CSV format or open it in a web browser for easy viewing.
5. The user can also copy the diet plan to the clipboard using the "pyperclip" library and paste it in an email or document using the "pyautogui" library. The user can also open the diet plan in a web browser using the "tempfile" and "webbrowser" libraries.

## Future Enhancement

We plan to add a graphical user interface (GUI) to improve the user experience.


## License

This project is licensed under the MIT License, which allows others to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software without restriction.
