from assertpy import soft_assertions
from pydantic import BaseModel


class Health(BaseModel):
    value: int = 0

    def __init__(self, value: int) -> None:
        super().__init__(value=value)
        with soft_assertions():
            assert type(value) is int
        self.value = value

    def __add__(self, other: "Health") -> "Health":
        """Перегрузка оператора '+' для сложения величины здоровья"""
        return Health(value=self.value + other.value)

    def __sub__(self, other: "Health") -> "Health":
        """Перегрузка оператора '-' для вычитания величины здоровья"""
        return Health(value=self.value - other.value)

    def __eq__(self, other: "Health") -> bool:
        """Перегрузка оператора '==' для сравнения величин здоровья"""
        return self.value == other.value if type(other) is Health else False

    def __ne__(self, other: "Health") -> bool:
        """Перегрузка оператора '!=' для сравнения величин здоровья"""
        return self.value != other.value if type(other) is Health else False

    def __lt__(self, other: "Health") -> bool:
        """Перегрузка оператора '<' для сравнения величин здоровья"""
        print(self.value, other.value)
        print(self.value < other.value)
        return self.value < other.value if type(other) is Health else False

    def __le__(self, other: "Health") -> bool:
        """Перегрузка оператора '<=' для сравнения величин здоровья"""
        return self.value <= other.value if type(other) is Health else False

    def __gt__(self, other: "Health") -> bool:
        """Перегрузка оператора '>' для сравнения величин здоровья"""
        return self.value > other.value if type(other) is Health else False

    def __ge__(self, other: "Health") -> bool:
        """Перегрузка оператора '>=' для сравнения величин здоровья"""
        return self.value >= other.value if type(other) is Health else False

    def __str__(self) -> str:
        return f"{self.value}"
