import pytest

from src.quadratic_equation import QuadraticEquation


class TestQuadraticEquation:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.solve = QuadraticEquation.solve

    def test_there_is_no_roots(self):
        """П3. Тест проверяет, что для уравнения x^2+1 = 0 корней нет."""
        assert self.solve(a=1, b=0, c=1) == []
