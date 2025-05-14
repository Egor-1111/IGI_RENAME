import numpy as np
import Input_data

"""
Find the number of even and odd numbers in the matrix.
What is the correlation coefficient between the even and odd
elements of the matrix?
"""
class Matrix:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.data = np.empty((rows, columns))

    def fill_random(self):
        self.data = np.random.randint(-100, 100, size=(self.rows, self.columns))

    def display(self):
        print(self.data)


class IntegerMatrix(Matrix):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.data = np.empty((rows, columns), dtype=int)

    def kol_chet_nechet(self):
        even = np.count_nonzero(self.data % 2 == 0)
        odd = np.count_nonzero(self.data % 2 != 0)
        return even, odd

    def correlation_even_odd(self):

        even_elements = self.data[self.data % 2 == 0]
        odd_elements = self.data[self.data % 2 != 0]

        min_len = min(len(even_elements), len(odd_elements))

        if min_len < 2:
            return None

        even_sample = even_elements[:min_len]
        odd_sample = odd_elements[:min_len]

        correlation_matrix = np.corrcoef(even_sample, odd_sample)
        return round(correlation_matrix[0, 1], 4)


def task5():
    m = Input_data.input_data("Введите количество столбцов матрицы: ", int, 1, 10000)
    n = Input_data.input_data("Введите количество строк матрицы: ", int, 1, 10000)

    integer_matrix = IntegerMatrix(m, n)
    integer_matrix.fill_random()
    print("Исходная матрица:")
    integer_matrix.display()
    even, odd = integer_matrix.kol_chet_nechet()
    print(f"\nКоличество четных чисел: {even}")
    print(f"Количество нечетных чисел: {odd}")
    correlation = integer_matrix.correlation_even_odd()
    if correlation is not None:
        print(f"Коэффициент корреляции между четными и нечетными элементами: {correlation}")
    else:
        print("Недостаточно данных для вычисления корреляции")
