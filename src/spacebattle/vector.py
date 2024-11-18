from assertpy import soft_assertions


class Vector:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        with soft_assertions():
            assert type(x) is int
            assert type(y) is int
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def __add__(self, other: "Vector") -> "Vector":
        """Перегрузка оператора '+' для сложения векторов"""
        self.__x += other.x
        self.__y += other.y
        return self

    def __eq__(self, other: "Vector") -> bool:
        """Перегрузка оператора == для сравнения векторов"""
        return other.x == self.__x and other.y == self.__y if type(other) is Vector else False

    def __str__(self) -> str:
        return f"({self.__x}, {self.__y})"
