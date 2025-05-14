import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt


def Task6():
    try:
        penguins = pd.read_csv('penguins_size.csv')
        print("Данные успешно загружены. Размер таблицы:", penguins.shape)
    except FileNotFoundError:
        print("Ошибка: Файл 'penguins_size.csv' не найден.")
        return

    print("Первые 5 строк данных:")
    display(penguins.head())

    print("\nИнформация о данных:")
    print(penguins.info())

    print("\nОписательная статистика числовых столбцов:")
    display(penguins.describe())

    print("\nКоличество пропущенных значений в каждом столбце:")
    display(penguins.isnull().sum())

    penguins_clean = penguins.dropna()
    print(f"\nУдалено строк с пропущенными значениями: {len(penguins) - len(penguins_clean)}")

    print("ЧАСТЬ 2: АНАЛИЗ ПО ВИДАМ ПИНГВИНОВ")

    species_group = penguins_clean.groupby('species')

    print("Средние показатели по видам:")
    display(species_group.mean(numeric_only=True))

    try:
        # Визуализация средних показателей
        print("\nСредняя длина клюва по видам:")
        species_group['culmen_length_mm'].mean().plot(kind='bar',
                                                      title='Средняя длина клюва (мм)')
        plt.show()

        print("\nСредняя масса тела по видам:")
        species_group['body_mass_g'].mean().plot(kind='bar',
                                                 title='Средняя масса тела (г)')
        plt.show()
    except Exception as e:
        print(f"\nОшибка при построении графиков: {str(e)}")

    print("ЧАСТЬ 3: СРАВНЕНИЕ САМЦОВ И САМОК")

    males = penguins_clean[penguins_clean['sex'] == 'MALE']
    females = penguins_clean[penguins_clean['sex'] == 'FEMALE']

    print("Средняя масса тела:")
    print(f"Самцы: {males['body_mass_g'].mean():.1f} г")
    print(f"Самки: {females['body_mass_g'].mean():.1f} г")
    print(f"Разница: {males['body_mass_g'].mean() - females['body_mass_g'].mean():.1f} г")

    print("\nСредняя длина плавника:")
    print(f"Самцы: {males['flipper_length_mm'].mean():.1f} мм")
    print(f"Самки: {females['flipper_length_mm'].mean():.1f} мм")


    print("ЧАСТЬ 4: АНАЛИЗ ПО ОСТРОВАМ")

    island_group = penguins_clean.groupby('island')

    print("Количество пингвинов на каждом острове:")
    display(island_group.size())

    try:
        print("\nСредняя глубина клюва по островам:")
        island_group['culmen_depth_mm'].mean().plot(kind='bar',
                                                    title='Средняя глубина клюва (мм)')
        plt.show()
    except Exception as e:
        print(f"\nОшибка при построении графика: {str(e)}")


    print("ЧАСТЬ 5: КОРРЕЛЯЦИОННЫЙ АНАЛИЗ")

    print("Матрица корреляций между числовыми параметрами:")
    corr_matrix = penguins_clean.select_dtypes(include=['float64', 'int64']).corr()
    display(corr_matrix)

    max_corr = corr_matrix.unstack().sort_values(ascending=False)
    max_corr = max_corr[max_corr != 1].head(3)
    print("\nТоп-3 наиболее коррелирующих пар параметров:")
    display(max_corr)

    print("\nАнализ завершен!")