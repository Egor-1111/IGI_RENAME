import Input_data
import math
import numpy as np
from tabulate import tabulate
from statistics import median, mode, variance, stdev
import matplotlib.pyplot as plt

"""
a) determination of additional parameters arithmetic mean of sequence elements, median, mode, variance, sequence COEX;
b) using the matplotlib library, draw graphs of different colors in the same coordinate axis:
"""
class SequenceAnalyzer:
    def __init__(self, sequence):
        self.sequence = sequence

    def calculate_mean(self):
        return sum(self.sequence) / len(self.sequence)

    def calculate_median(self):
        return median(self.sequence)

    def calculate_mode(self):
        return mode(self.sequence)

    def calculate_variance(self):
        return variance(self.sequence)

    def calculate_standard_deviation(self):
        return stdev(self.sequence)


def calculate_actual_value(x):
    return math.log(1 - x)


class SequenceCalculator(SequenceAnalyzer):
    def __init__(self, max_iterations, eps):
        super().__init__([])
        self.max_iterations = max_iterations
        self.eps = eps

    def calculate_sequence(self, x):
        result = 0
        n = 1
        term = -x
        while abs(term) > self.eps and n <= self.max_iterations:
            result += term
            term = - (x ** (n + 1)) / (n + 1)
            self.sequence.append(result)
            n += 1
        return result

    def generate_table(self, x, result, actual_value):
        table_data = [[x, len(self.sequence), result, actual_value, self.eps]]
        table_headers = ["x", "Итерации", "F(x)", "Математический F(x)", "Точность"]
        table = tabulate(table_data, headers=table_headers, floatfmt=".8f")
        return table


def Task3():
    max_iterations = 500
    while True:
        x = Input_data.input_data("Введите x: ", float, -1, 1)
        if x == -1:
            print("Ошибка: Значение должно быть больше или равно -1. Пожалуйста, введите корректное значение.")
        elif x == 1:
            print("Ошибка: Значение должно быть меньше или равно 1. Пожалуйста, введите корректное значение.")
        else:
            break
    eps = Input_data.input_data("Введите eps: ", float, None, 1)
    if eps == 1:
        print("Ошибка: Значение должно быть меньше 1. Пожалуйста, введите корректное значение.")

    calculator = SequenceCalculator(max_iterations, eps)
    result = calculator.calculate_sequence(x)
    actual_value = calculate_actual_value(x)
    table = calculator.generate_table(x, result, actual_value)

    print(table)
    print("Среднее арифметическое:", calculator.calculate_mean())
    print("Медиана:", calculator.calculate_median())
    print("Мода:", calculator.calculate_mode())
    print("Дисперсия:", calculator.calculate_variance())
    print("Стандартное отклонение:", calculator.calculate_standard_deviation())

    x_values = np.linspace(0, 1, len(calculator.sequence))
    y_values = calculator.sequence

    plt.plot(x_values, y_values, color="blue", label="Ряд")
    plt.plot(x_values, [calculate_actual_value(x)] * len(calculator.sequence), color="red",linestyle="--", label="Математический F(x)")
    plt.xlabel('n')
    plt.ylabel('F(x)')
    plt.legend()
    plt.grid(True)
    plt.title("График разложения функции в ряд")

    plt.savefig("Task3.png")

    plt.show()