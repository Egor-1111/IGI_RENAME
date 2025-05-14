import csv
import pickle
import Input_data


"""
The source data is a dictionary. You need to put them in a file using a serializer.  
 Organize data reading, searching, and sorting according to an individual task. Be sure to use classes. 
 Implement two options: 1)CSV file format; 2)pickle module

Implement a table of dates and events of the Belarusian history. 
Create a program that displays a list of events entered from the keyboard.
"""
class HistoryEvent:

    def __init__(self,year,description):
        self.year = year
        self.description = description

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self,value):
        self._description = value

    def get_century(self):
        return (self.year - 1) // 100 + 1

    def  get_info(self):
        print(f"Год: {self.year}")
        print(f"Событие: {self.description}")
        print("--------------------")

class HistoryDatabase:
    def __init__(self):
        self.events = []

    def add_event(self,event):
        self.events.append(event)

    def show_events(self):
        for event in self.events:
            event.get_info()

    def sort_by_year(self):
        self.events.sort(key=lambda x: x.year)

    def get_events_by_century(self, century):
        return [event for event in self.events if event.get_century() == century]

def save_to_csv(event_list):

    with open("history.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Год", "Событие"])
        for event in event_list:
            writer.writerow([event.year, event.description])
    print("Данные успешно сохранены в файл history.csv.")

def load_from_csv():

    event_list = []
    try:
        with open("history.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовок
            for row in reader:
                if row:  # Проверка на пустые строки
                    event = HistoryEvent(int(row[0]), row[1])
                    event_list.append(event)
    except FileNotFoundError:
        print("Файл history.csv не найден.")
    return event_list

def save_to_pickle(event_list):

    with open("history.pickle", mode="wb") as file:
        pickle.dump(event_list, file)
    print("Данные успешно сохранены в файл history.pickle.")


def load_from_pickle():

    try:
        with open("history.pickle", mode="rb") as file:
            event_list = pickle.load(file)
    except FileNotFoundError:
        print("Файл history.pickle не найден.")
        event_list = []
    return event_list

def Task1():
    db = HistoryDatabase()

    sample_events = [
        (862, "Первое упоминание о Полоцке"),
        (1240, "Битва на реке Немиге"),
        (1569, "Люблинская уния"),
        (1794, "Восстание Костюшко"),
        (1863, "Восстание Калиновского"),
        (1918, "Провозглашение БНР"),
        (1945, "Окончание Великой Отечественной войны"),
        (1991, "Провозглашение независимости Беларуси")
    ]

    for year,description in sample_events:
        db.add_event(HistoryEvent(year,description))

    while True:
        print("\nМеню работы с историческими событиями Беларуси")
        print("1. Добавить событие")
        print("2. Показать все события")
        print("3. Отсортировать события по году")
        print("4. Найти события по веку")
        print("5. Сохранить данные в CSV")
        print("6. Загрузить данные из CSV")
        print("7. Сохранить данные в pickle")
        print("8. Загрузить данные из pickle")
        print("0. Выход")
        choice = Input_data.input_data("Выберите пункт меню: ", int, 0, 8)

        if choice == 1:
            year_and_description_data = {"year":Input_data.input_data("Введите год события: ",int,0,2025),
                                         "description":Input_data.input_data("Введите описание события: ",str)}
            db.add_event(HistoryEvent(year_and_description_data["year"],year_and_description_data["description"]))
            print("Событие успешно добавлено!")

        elif choice == 2:
            print("\nВсе исторические события:")
            db.show_events()

        elif choice == 3:
            db.sort_by_year()
            db.show_events()
            print("Отсортированно по году")

        elif choice == 4:
            century = Input_data.input_data("Введите век (например, 19 для XIX века): ", int, 1, 21)
            events = db.get_events_by_century(century)
            if events:
                print(f"\nСобытия {century} века:")
                for event in events:
                    event.get_info()
            else:
                print(f"В {century} веке нет событий в базе данных.")

        elif choice == 5:
            save_to_csv(db.events)

        elif choice == 6:
            db.events = load_from_csv()

        elif choice == 7:
            save_to_pickle(db.events)

        elif choice == 8:
            db.events = load_from_pickle()


        elif choice == 0:
            print("Программа завершена.")
            break




