class Matrix:
    def __init__(self, data):
        # Принимает список списков
        self.matrix = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0


    def str(self):
        """Переопределение вывода матрицы."""
        return "\n".join(["\t".join(map(str, row)) for row in self.matrix])

    def size(self):
        """Возвращает размерность матрицы (кортеж)."""
        return (self.rows, self.cols)

    def count_elements(self):
        """Возвращает кол-во элементов в матрице."""
        return self.rows * self.cols

    def total_sum(self):
        """Возвращает сумму всех элементов матрицы."""
        return sum(sum(row) for row in self.matrix)

    # --- Математические операции (Синий цвет - возвращают новый экземпляр) ---

    def add(self, other):
        """Сложение матриц одинаковых размерностей."""
        if self.size() != other.size():
            raise ValueError("Матрицы должны быть одинакового размера")

        result = [
            [self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def subtract(self, other):
        """Вычитание матриц."""
        if self.size() != other.size():
            raise ValueError("Матрицы должны быть одинакового размера")

        result = [
            [self.matrix[i][j] - other.matrix[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def multiply_by_number(self, number):
        """Умножение матрицы на число."""
        result = [
            [self.matrix[i][j] * number for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def transpose(self):
        """Транспонирование матрицы."""
        result = [
            [self.matrix[i][j] for i in range(self.rows)]
            for j in range(self.cols)
        ]
        return Matrix(result)

    def replace_negatives_with_zero(self):
        """Возвращает новую матрицу, где вместо отрицательных чисел стоят нули."""
        result = [
            [max(0, self.matrix[i][j]) for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)



    def eq(self, other):
        """Возможность сравнения на равенство двух матриц."""
        if not isinstance(other, Matrix) or self.size() != other.size():
            return False
        return self.matrix == other.matrix


    @classmethod
    def identity(cls, n, m=None):
        """Создает единичную матрицу размером n x m (или n x n)."""
        if m is None: m = n
        data = [[1 if i == j else 0 for j in range(m)] for i in range(n)]
        return cls(data)

    @classmethod
    def zero(cls, n, m):
        """Создает нулевую матрицу размером n, m."""
        data = [[0 for _ in range(m)] for _ in range(n)]
        return cls(data)

    @classmethod
    def diagonal(cls, diag_list):
        """Создает диагональную матрицу из переданного списка."""
        n = len(diag_list)
        data = [[diag_list[i] if i == j else 0 for j in range(n)] for i in range(n)]
        return cls(data)


#Примеры использования

m1 = Matrix([[-1, 3], [0, 1], [-2, 2]])
m2 = Matrix([[2, 0], [-1, 1], [3, -2]])

print("Матрица 1:\n", m1, sep="")
print("\nСложение:\n", m1.add(m2), sep="")
print("\nТранспонирование M1:\n", m1.transpose(), sep="")
print("\nЗамена отрицательных на 0:\n", m1.replace_negatives_with_zero(), sep="")

eye = Matrix.identity(3)
print("\nЕдиничная матрица 3x3:\n", eye, sep="")
