import pytest

from src.spacebattle.exceptions.exeptions import ZeroValueError
from src.spacebattle.qe.quadratic_equation import QuadraticEquation

_ALL_TYPES = (
    None,
    True,
    "str",
    (1,),
    bytes(b"bytes"),
    frozenset(range(2)),
    [1, 2],
    {1: 2},
    set(range(2)),
    bytearray(b"bytearray"),
)

data_for_test = []
for arg_ in range(4):
    for type_ in _ALL_TYPES:
        if arg_ == 0:
            data_for_test.append((type_, 1, 1, 1))
        elif arg_ == 1:
            data_for_test.append((1, type_, 1, 1))
        if arg_ == 2:
            data_for_test.append((1, 1, type_, 1))
        if arg_ == 3:
            data_for_test.append((1, 1, 1, type_))


class TestQuadraticEquation:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.solve = QuadraticEquation.solve

    def test_there_is_no_roots(self):
        """П3. Тест проверяет, что для уравнения x^2+1 = 0 корней нет."""
        assert self.solve(a=1, b=0, c=1) == []

    def test_there_are_two_roots(self):
        """П5. Тест проверяет, что для уравнения x^2-1 = 0 есть два корня."""
        assert self.solve(a=1, b=0, c=-1) == (1.0, -1.0)

    def test_there_is_one_root(self):
        """П7. Тест проверяет, что для уравнения x^2+2x+1 = 0 есть один корень."""
        assert self.solve(a=2, b=3, c=1, e=1.5) == (-0.75, -0.75)

    def test_coefficient_cannot_be_equal_to_zero(self):
        """П9. Тест проверяет, что коэффициент 'a' не может быть равен 0."""
        with pytest.raises(ZeroValueError):
            self.solve(a=0, b=0, c=0)

    @pytest.mark.parametrize(
        "a, b, c, e", data_for_test, ids=[f"{type(val[0])} {type(val[1])} {type(val[2])}" for val in data_for_test]
    )
    def test_another_types(self, a, b, c, e):
        """П13. Тест проверяет что другие типы данных (отличные от int и float) аргументов не валидны."""
        with pytest.raises(AssertionError):
            self.solve(a, b, c, e)
