def input_data(prompt, data_type, min_value=None, max_value=None):

    while True:
        try:
            user_input = data_type(input(prompt))
            if min_value is not None and user_input < min_value:
                raise ValueError(f"Value must be at least {min_value}")
            if max_value is not None and user_input > max_value:
                raise ValueError(f"Value must be at most {max_value}")
            return user_input
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid value.")