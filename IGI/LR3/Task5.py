import Input_data

"""
The program should contain the following basic functions:
1) user input of list items;
2) checking the correctness of the input data;
3) implementation of the main task with the output of the results;
4) Display the list on the screen.

Find the number of the maximum modulo element of the list and the product of the elements located between the first and second zero elements
"""
def Task5():
    choice = Input_data.Input_data("Напишите 1 для ручного ввода, 2 для автоматического ввода: ", int, 1, 2)
    numbers = list()
    if choice == 1:
        while True:
            number = Input_data.Input_data("Введите число с плавающей запятой (для завершения введите 333)", float,None,None)
            if number == 333:
                break
            numbers.append(number)

    elif choice == 2:
        while True:
            number_generator = Input_data.Random_Generator(float, -10000, 10000, 20)
            numbers = list(number_generator)
            break

    zero_indices = [i for i, x in enumerate(numbers) if x == 0]
    if len(zero_indices) < 2:
        print("Не хватает нулей")
        return None, None


    start, end = zero_indices[0], zero_indices[1]
    sublist = numbers[start + 1:end]

    max_abs_val = max(sublist, key=abs)
    max_abs_index = numbers.index(max_abs_val)

    product = 1
    for num in sublist:
        product *= num

    print(f"Номер максимального элемента по модулю между нулями: {max_abs_index} (значение: {numbers[max_abs_index]})")
    print(f"Произведение элементов между нулями: {product}")