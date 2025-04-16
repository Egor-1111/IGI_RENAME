import Input_data

"""
Organize a loop that accepts integers from the keyboard and counts the number of even numbers. 
The end of the loop is entering a number greater than 1000.
And find the sum of the sequence.
"""

def Task2():
    choice = Input_data.Input_data("Напишите 1 для ручного ввода, 2 для автоматического ввода: ", int, 1, 2)
    numbers = list()
    if choice == 1:
        while True:
            number = Input_data.Input_data("Введите число", int)
            if number > 1000:
                break
            elif number % 2 == 0:
                numbers.append(number)

    elif choice == 2:
        while True:
            number_generator = Input_data.Random_Generator(int,0,1100,20)
            all_numbers = list(number_generator)
            print(all_numbers)
            for i in all_numbers:
                if i > 1000:
                    break
                elif i % 2 == 0:
                    numbers.append(i)
            break

    print(f"Количество четных элементов {len(numbers)}")
    print(f"Сумма элементов {sum(numbers)}")

