from assertpy import soft_assertions
from pydantic import BaseModel


class Vector(BaseModel):
    x: int = 0
    y: int = 0

    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(x=x, y=y)
        with soft_assertions():
            assert type(x) is int
            assert type(y) is int
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        """Перегрузка оператора '+' для сложения векторов"""
        return Vector(x=self.x + other.x, y=self.y + other.y)

    def __eq__(self, other: "Vector") -> bool:
        """Перегрузка оператора == для сравнения векторов"""
        return other.x == self.x and other.y == self.y if type(other) is Vector else False

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y})"
