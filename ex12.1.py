# 1
class Soda:
    def __init__(self, additive=None):
        # Проверяем, является ли добавка строкой
        if isinstance(additive, str):
            self.additive = additive
        else:
            self.additive = None

    def show_my_drink(self):
        if self.additive:
            print(f"Газировка и {self.additive}")
        else:
            print("Обычная газировка")

            # 2

        class TriangleChecker:

    def __init__(self, sides):
        self.sides = sides

    def is_triangle(self):
        if not all(isinstance(x, (int, float)) for x in self.sides):
            return "Нужно вводить только числа!"

        if any(x <= 0 for x in self.sides):
            return "С отрицательными числами ничего не выйдет!"

        a, b, c = sorted(self.sides)
        if a + b > c:
            return "Ура, можно построить треугольник!"
        else:
            return "Жаль, но из этого треугольник не сделать."


# 3
class KgToPounds:
    def __init__(self, kg):
        self.__kg = kg  # Приватная переменная

    def to_pounds(self):
        return self.__kg * 2.205

    def set_kg(self, new_kg):
        if isinstance(new_kg, (int, float)):
            self.__kg = new_kg
        else:
            print("Записывать можно только числовые значения!")

    def get_kg(self):
        return self.__kg


# 3.2

class KgToPoundsProperty:
    def __init__(self, kg):
        self.__kg = kg

    @property
    def kg(self):
        return self.__kg

    @kg.setter
    def kg(self, new_kg):
        if isinstance(new_kg, (int, float)):
            self.__kg = new_kg
        else:
            print("Ошибка: введите число!")

    def to_pounds(self):
        return self.__kg * 2.205


# 4
class RealString:
    def __init__(self, string):
        self.string = str(string)

    def len(self):
        return len(self.string)

    def eq(self, other):
        return len(self) == len(other)

    def lt(self, other):
        return len(self) < len(other)

    def le(self, other):
        return len(self) <= len(other)

    def gt(self, other):
        return len(self) > len(other)

    def ge(self, other):
        return len(self) >= len(other)


# 5

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def str(self):
        return f"Прямоугольник с шириной {self.width} и высотой {self.height}"

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2 * (self.width + self.height)

    @property
    def is_square(self):
        return self.width == self.height


# 6

class Person:
    def __init__(self, name, age, gender):
        self._name = name
        self.age = age
        self.gender = gender

    def str(self):
        return f"Имя: {self._name}, Возраст: {self.age}, Пол: {self.gender}"

    def get_name(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @staticmethod
    def is_adult(age):
        return age >= 18

    @classmethod
    def create_from_string(cls, s):
        name, age, gender = s.split('-')
        return cls(name, int(age), gender)
