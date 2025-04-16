import Input_data
import string

"""
Count the number of whitespace characters in a line entered from the keyboard.
"""

def Task3():
    global user_input
    choice = Input_data.Input_data("Напишите 1 для ручного ввода, 2 для автоматического ввода: ", int, 1, 2)
    if choice == 1:
        user_input = Input_data.Input_data("Введите строку: ", str, None, None)
    elif choice == 2:
        user_input = next(Input_data.Random_Generator(str, 10, 50,1))
        print(user_input)

    blank_space_count = user_input.count(" ")
    print(f"Количество пробелов {blank_space_count}")

