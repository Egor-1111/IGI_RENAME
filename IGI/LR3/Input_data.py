import  random
import  string
from typing import Iterator, Union, Optional

def Input_data(prompt,data_type,min_value=None,max_value=None):
    while True:
        try:
            user_input = data_type(input(prompt))
            if min_value is not None and user_input < min_value:
                raise ValueError(f"Значение должно быть не менее {min_value}")
            if max_value is not None and user_input > max_value:
                raise ValueError(f"Значение должно быть не более {max_value}")
            return user_input
        except ValueError as e:
            print(f"Ошибка:{e}. Пожалуйста введите валидное значение.")


def Random_Generator(
    data_type: type,
    min_value: Optional[Union[int, float]] = None,
    max_value: Optional[Union[int, float]] = None,
    count: Optional[int] = None
) -> Iterator[Union[str, int, float]]:
    """Генератор случайных значений указанного типа"""
    # Обработка строк
    if data_type == str:
        min_len = min_value if min_value is not None else 1
        max_len = max_value if max_value is not None else 10
        chars = string.ascii_letters + string.digits + " "

        for i in range(count) if count is not None else iter(int, 1):
            length = random.randint(min_len, max_len)
            yield ''.join(random.choices(chars, k=length))
    else:
        min_val = min_value if min_value is not None else float('-inf')
        max_val = max_value if max_value is not None else float('inf')

        if min_val > max_val:
            raise ValueError("минимальное значение не может быть больше максимального значения")

        for _ in range(count) if count is not None else iter(int, 1):
            if data_type == int:
                yield random.randint(int(min_val), int(max_val))
            elif data_type == float:
                yield random.uniform(min_val, max_val)
            else:
                raise ValueError("Неподдерживаемый тип данных. Используйте str, int или float")