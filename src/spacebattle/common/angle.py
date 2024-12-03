from assertpy import soft_assertions


class Angle:
    def __init__(self, d: int = 0, n: int = 1) -> None:
        with soft_assertions():
            assert type(d) is int
            assert type(n) is int
            assert d < n, "Угол поворота должен 'd' быть меньше кол-ва частей 'n'"
        self.d = d
        self.n = n

    def __add__(self, other: "Angle") -> "Angle":
        """Перегрузка оператора '+' для сложения углов"""
        assert self.n == other.n, "Кол-во частей 'n' должно быть одинаковым"
        return Angle(d=(self.d + other.d) % self.n, n=self.n)

    def __eq__(self, other: "Angle") -> bool:
        """Перегрузка оператора == для сравнения углов"""
        return other.d == self.d and other.n == self.n if type(other) is Angle else False

    def __str__(self) -> str:
        return f"({self.d}, {self.n})"

    def __repr__(self) -> str:
        return f"Angle(d={self.d}, n={self.n})"
