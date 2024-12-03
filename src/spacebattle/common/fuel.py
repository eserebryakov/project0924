from assertpy import soft_assertions


class Fuel:
    def __init__(self, value: int) -> None:
        with soft_assertions():
            assert type(value) is int
        self.value = value

    def __add__(self, other: "Fuel") -> "Fuel":
        """Перегрузка оператора '+' для сложения величины топлива"""
        return Fuel(value=self.value + other.value)

    def __sub__(self, other: "Fuel") -> "Fuel":
        """Перегрузка оператора '-' для вычитания величины топлива"""
        return Fuel(value=self.value - other.value)

    def __eq__(self, other: "Fuel") -> bool:
        """Перегрузка оператора '==' для сравнения величин топлива"""
        return self.value == other.value if type(other) is Fuel else False

    def __ne__(self, other: "Fuel") -> bool:
        """Перегрузка оператора '!=' для сравнения величин топлива"""
        return self.value != other.value if type(other) is Fuel else False

    def __lt__(self, other: "Fuel") -> bool:
        """Перегрузка оператора '<' для сравнения величин топлива"""
        return self.value < other.value if type(other) is Fuel else False

    def __le__(self, other: "Fuel") -> bool:
        """Перегрузка оператора '<=' для сравнения величин топлива"""
        return self.value <= other.value if type(other) is Fuel else False

    def __gt__(self, other: "Fuel") -> bool:
        """Перегрузка оператора '>' для сравнения величин топлива"""
        return self.value > other.value if type(other) is Fuel else False

    def __ge__(self, other: "Fuel") -> bool:
        """Перегрузка оператора '>=' для сравнения величин топлива"""
        return self.value >= other.value if type(other) is Fuel else False

    def __str__(self) -> str:
        return f"{self.value}"
