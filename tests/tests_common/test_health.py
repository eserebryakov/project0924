import sys

import pytest
from pydantic import ValidationError

from src.spacebattle.common.health import Health

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


class TestHealth:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.health = Health

    @pytest.mark.parametrize("value", _ACCEPTABLE_VALUES)
    def test_acceptable_values(self, value):
        """Тест проверяет допустимые значения для величины здоровья"""
        assert self.health(value)

    @pytest.mark.parametrize("value", _UNACCEPTABLE_VALUES, ids=[f"x={value}" for value in _UNACCEPTABLE_VALUES])
    def test_unacceptable_values(self, value):
        """Тест проверяет недопустимые значения для величины здоровья"""
        with pytest.raises((ValidationError, AssertionError)):
            assert self.health(value)

    def test_acceptable_add_health(self):
        """Тест проверяет успешную операцию '+' сложения здоровья"""
        health_ = self.health(5) + self.health(3)
        assert health_ == Health(8)

    def test_acceptable_sub_health(self):
        """Тест проверяет успешную операцию '-' вычитания здоровья"""
        health_ = self.health(5) - self.health(3)
        assert health_ == Health(2)

    def test_acceptable_equals_health(self):
        """Тест проверяет успешную операцию '==' эквивалентности здоровья"""
        assert self.health(1) == self.health(1)

    def test_acceptable_not_equals_health(self):
        """Тест проверяет успешную операцию '!=' неэквивалентности здоровья"""
        assert self.health(1) != self.health(5)

    def test_acceptable_lt_health(self):
        """Тест проверяет успешную операцию '<' неравенства здоровья"""
        assert self.health(1) < self.health(5)

    def test_acceptable_le_health(self):
        """Тест проверяет успешную операцию '<=' неравенства здоровья"""
        assert self.health(2) <= self.health(2)

    def test_acceptable_gt_health(self):
        """Тест проверяет успешную операцию '>' неравенства здоровья"""
        assert self.health(3) > self.health(2)

    def test_acceptable_ge_health(self):
        """Тест проверяет успешную операцию '>=' неравенства здоровья"""
        assert self.health(2) >= self.health(2)

    def test_valid_data_display(self):
        """Тест проверяет корректное отображение величины здоровья на экране"""
        assert str(self.health(1)) == "1"
