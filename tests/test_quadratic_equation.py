import pytest

from src.exeptions import ZeroValueError
from src.quadratic_equation import QuadraticEquation


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
        assert self.solve(a=1, b=2, c=1) == (-1.0, -1.0)

    def test_coefficient_cannot_be_equal_to_zero(self):
        """П9. Тест проверяет, что коэффициент 'a' не может быть равен 0."""
        with pytest.raises(ZeroValueError):
            self.solve(a=0, b=0, c=0)
