import sys

import pytest
from assertpy import soft_assertions

from src.spacebattle.common.fuel import Fuel

# Допустимые значения типов данных (позитивный тест)
_ACCEPTABLE_VALUES = (sys.maxsize, -sys.maxsize - 1, -1, 0, 1)

# Недопустимые значения типов данных (негативный тест)
_UNACCEPTABLE_VALUES = (
    0.1,
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


class TestAngle:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.fuel = Fuel

    @pytest.mark.parametrize("value", _ACCEPTABLE_VALUES)
    def test_acceptable_values(self, value):
        """Тест проверяет допустимые значения для величины топлива"""
        assert self.fuel(value)

    @pytest.mark.parametrize("value", _UNACCEPTABLE_VALUES, ids=[f"x={value}" for value in _UNACCEPTABLE_VALUES])
    def test_unacceptable_values(self, value):
        """Тест проверяет недопустимые значения для величины топлива"""
        with pytest.raises(AssertionError):
            assert self.fuel(value)

    def test_acceptable_add_fuel(self):
        """Тест проверяет успешную операцию '+' сложения топлива"""
        fuel_ = self.fuel(5) + self.fuel(3)
        with soft_assertions():
            assert fuel_ == Fuel(8)

    def test_acceptable_sub_fuel(self):
        """Тест проверяет успешную операцию '-' вычитания топлива"""
        fuel_ = self.fuel(5) - self.fuel(3)
        with soft_assertions():
            assert fuel_ == Fuel(2)

    def test_acceptable_equals_fuel(self):
        """Тест проверяет успешную операцию '==' эквивалентности топлива"""
        assert self.fuel(1) == self.fuel(1)

    def test_acceptable_not_equals_fuel(self):
        """Тест проверяет успешную операцию '!=' неэквивалентности топлива"""
        assert self.fuel(1) != self.fuel(5)

    def test_acceptable_lt_fuel(self):
        """Тест проверяет успешную операцию '<' неравенства топлива"""
        assert self.fuel(1) < self.fuel(5)

    def test_acceptable_le_fuel(self):
        """Тест проверяет успешную операцию '<=' неравенства топлива"""
        assert self.fuel(2) <= self.fuel(2)

    def test_acceptable_gt_fuel(self):
        """Тест проверяет успешную операцию '>' неравенства топлива"""
        assert self.fuel(3) > self.fuel(2)

    def test_acceptable_ge_fuel(self):
        """Тест проверяет успешную операцию '>=' неравенства топлива"""
        assert self.fuel(2) >= self.fuel(2)

    def test_valid_data_display(self):
        """Тест проверяет корректное отображение величины топлива на экране"""
        assert str(self.fuel(1)) == "1"
