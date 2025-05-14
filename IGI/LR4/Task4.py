import math
from abc import ABC, abstractmethod
from matplotlib import pyplot as plt
import Input_data

"""
Construct a triangle on the sides a, b and the angle between them C (in degrees).
"""
class GeometricFigure(ABC):
    @abstractmethod
    def calculate_area(self):
        pass


class FigureColor:
    def __init__(self, color):
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value


class Triangle(GeometricFigure):
    _figure_name = "Треугольник"

    def __init__(self, color, side_a, side_b, angle_c):
        self.color = FigureColor(color)
        self.side_a = side_a
        self.side_b = side_b
        self.angle_c = math.radians(angle_c)

    @property
    def figure_name(self):
        return self._figure_name

    @figure_name.setter
    def figure_name(self, value):
        self._figure_name = value

    def calculate_area(self):
        return 0.5 * self.side_a * self.side_b * math.sin(self.angle_c)

    def draw(self):

        x1, y1 = 0, 0
        x2, y2 = self.side_a, 0
        x3 = self.side_b * math.cos(self.angle_c)
        y3 = self.side_b * math.sin(self.angle_c)

        x = [x1, x2, x3, x1]
        y = [y1, y2, y3, y1]

        color_map = {
            "красный": "red",
            "зеленый": "green",
            "синий": "blue",
            "черный": "black",
            "желтый": "yellow"
        }

        plt.fill(x, y, color_map.get(self.color.color, "blue"))
        plt.axis("equal")

        margin = max(self.side_a, self.side_b) * 0.1
        plt.xlim(min(x) - margin, max(x) + margin)
        plt.ylim(min(y) - margin, max(y) + margin)

        plt.text(sum(x) / 3, min(y) - margin / 2, self.figure_name, ha="center")
        plt.savefig("triangle.png")
        plt.show()

    def __str__(self):
        return "{} со сторонами {} и {} единиц, углом {} градусов, цвет: {}, площадь: {:.2f} кв.ед.".format(
            self.figure_name, self.side_a, self.side_b, math.degrees(self.angle_c),
            self.color.color, self.calculate_area()
        )


def Task4():
    name = Input_data.input_data("Введите название фигуры: ", str)
    side_a = Input_data.input_data("Введите длину стороны a: ", int, 0)
    side_b = Input_data.input_data("Введите длину стороны b: ", int, 0)
    angle_c = Input_data.input_data("Введите угол между сторонами (в градусах): ", int, 0, 91)

    allowed_colors = ["красный", "зеленый", "синий", "черный", "желтый"]
    color = Input_data.input_data(
        "Введите цвет фигуры (красный, зеленый, синий, черный, желтый): ", str
    ).lower()

    while color not in allowed_colors:
        print("Недопустимый цвет! Попробуйте снова.")
        color = Input_data.input_data(
            "Введите цвет фигуры (красный, зеленый, синий, черный, желтый): ", str
        ).lower()

    triangle = Triangle(color, side_a, side_b, angle_c)
    triangle.figure_name = name
    print(triangle)
    triangle.draw()