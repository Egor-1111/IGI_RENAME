import Task1
import Task2
import Task3
import Task4
import Task5
import Input_data
"""
14.04.2025 Borovikov Egor Variant 4
"""


def main_menu():
    while True:
        print("Меню")
        print("1. Задание 1")
        print("2. Задание 2")
        print("3. Задание 3")
        print("4. Задание 4")
        print("5. Задание 5")
        print("0. Выход")

        choice = Input_data.Input_data("Введите номер задания: ", int, 0, 5)

        if choice == 1:
            Task1.Task1()
        elif choice == 2:
            Task2.Task2()
        elif choice == 3:
            Task3.Task3()
        elif choice == 4:
            Task4.Task4()
        elif choice == 5:
            Task5.Task5()
        elif choice == 0:
            print("Выход из программы...")
            break