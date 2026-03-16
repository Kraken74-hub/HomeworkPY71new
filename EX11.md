import time

class Auto:

    def __init__(self, brand: object, age: object, mark: object, color: object = None, weight: object = None) -> None:
        self.brand = brand
        self.age = age
        self.mark = mark
        self.color = color
        self.weight = weight

    def move(self):
        print("move")

    def stop(self):
        print("stop")

    def birthday(self):
        self.age += 1

#Класс Truck
class Truck(Auto):
    def __init__(self, brand, age, mark, max_load, color=None, weight=None):
        # Вызываем конструктор родителя
        super().__init__(brand, age, mark, color, weight)
        self.max_load = max_load

    def move(self):
        print("attention")
        super().move()

    def load(self):
        time.sleep(1)
        print("load")
        time.sleep(1)

#Класс Car
class Car(Auto):
    def __init__(self, brand, age, mark, max_speed, color=None, weight=None):
        super().__init__(brand, age, mark, color, weight)
        self.max_speed = max_speed

    def move(self):
        super().move()
        print(f"max speed is {self.max_speed}")

# Проверка

print("ТЕСТ ГРУЗОВИКОВ")
truck1 = Truck("Mercedes", 5, "Actros", 20000, "White", 8000)
truck2 = Truck("Volvo", 2, "FH16", 15000)

for t in [truck1, truck2]:
    print(f"Грузовик: {t.brand} {t.mark}, Возраст: {t.age}, Груз: {t.max_load}")
    t.move()
    t.load()
    t.stop()
    t.birthday()
    print(f"Новый возраст: {t.age}\n")

print("ТЕСТ ЛЕГКОВЫХ АВТО")
car1 = Car("Tesla", 1, "Model 3", 225, "Red")
car2 = Car("BMW", 4, "M5", 305, weight=1900)

for c in [car1, car2]:
    print(f"Машина: {c.brand} {c.mark}, Возраст: {c.age}, Скорость: {c.max_speed}")
    c.move()
    c.stop()
    c.birthday()
    print(f"Новый возраст: {c.age}\n")
