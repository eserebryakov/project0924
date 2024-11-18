from assertpy import soft_assertions


class Angle:
    def __init__(self, d: int = 0, n: int = 1) -> None:
        with soft_assertions():
            assert type(d) is int
            assert type(n) is int
            assert d < n, "Угол поворота должен 'd' быть меньше кол-ва частей 'n'"
        self.__d = d
        self.__n = n

    @property
    def d(self) -> int:
        return self.__d

    @property
    def n(self) -> int:
        return self.__n

    def __add__(self, other: "Angle") -> "Angle":
        """Перегрузка оператора '+' для сложения углов"""
        assert self.__n == other.n, "Кол-во частей 'n' должно быть одинаковым"
        self.__d = (self.d + other.d) % self.__n
        return self

    def __eq__(self, other: "Angle") -> bool:
        """Перегрузка оператора == для сравнения углов"""
        return other.d == self.__d and other.n == self.__n if type(other) is Angle else False

    def __str__(self) -> str:
        return f"({self.__d}, {self.__n})"
