import math
import Input_data
from tabulate import tabulate
"""
Calculating the value of a function by decomposing a function into a power series. Set the accuracy of eps calculations.
Provide for a maximum number of iterations of 500.
Print the number of terms of the series required to achieve the specified calculation accuracy.
"""

def Task1():
    max_iterations = 500
    choice = Input_data.Input_data("Напишите 1 для ручного ввода, 2 для автоматического ввода: ", int, 1, 2)
    if choice == 1:
        while True:
            x = Input_data.Input_data("Введите x: ", float, -1, 1)
            if x == -1:
                print("Ошибка: Значение должно быть не менее -1. Пожалуйста, введите допустимое значение.")
            elif x == 1:
                print("Ошибка: Значение должно быть не более 1. Пожалуйста, введите допустимое значение.")
            else:
                break

        eps = Input_data.Input_data("Введите eps: ", float, None, 1)
    elif choice == 2:
        x = next(Input_data.Random_Generator(float, -0.999999999999999, 0.9999999999999999,1))
        eps = next(Input_data.Random_Generator(float, 0, 1,1))
    result = 0
    n = 1
    term = -x
    while abs(term) > eps and n <= max_iterations:
        result += term
        term = - (x ** (n + 1)) / (n + 1)
        n += 1

    math_value = math.log(1 - x)
    table_data = [
        [x, n, result, math_value, eps]
    ]
    table_headers = ["x", "n", "F(x)", "Math F(x)", "eps"]
    table = tabulate(table_data, headers=table_headers, floatfmt=".8f")

    print(table)