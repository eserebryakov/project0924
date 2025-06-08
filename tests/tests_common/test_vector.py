import itertools
import sys

import pytest
from assertpy import soft_assertions
from pydantic import ValidationError

from src.spacebattle.common.vector import Vector

# Допустимые значения типов данных (позитивный тест)
_ACCEPTABLE_VALUES = (sys.maxsize, -sys.maxsize - 1, -1, 0, 1)
_LIST_ACCEPTABLE_VALUES = (_ACCEPTABLE_VALUES, _ACCEPTABLE_VALUES)
_ACCEPTABLE_DATA_FOR_TEST = list(itertools.product(*_LIST_ACCEPTABLE_VALUES))

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
_LIST_UNACCEPTABLE_VALUES = (_UNACCEPTABLE_VALUES, _UNACCEPTABLE_VALUES)
_UNACCEPTABLE_DATA_FOR_TEST = list(itertools.product(*_LIST_UNACCEPTABLE_VALUES))


class TestVector:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.vector = Vector

    @pytest.mark.parametrize(
        "x, y", _ACCEPTABLE_DATA_FOR_TEST, ids=[f"x={value[0]}, y={value[1]}" for value in _ACCEPTABLE_DATA_FOR_TEST]
    )
    def test_acceptable_values(self, x, y):
        """Тест проверяет допустимые граничные значения координат x, y: max, min, -1, 0 1"""
        assert self.vector(x, y)

    @pytest.mark.parametrize(
        "x, y",
        _UNACCEPTABLE_DATA_FOR_TEST,
        ids=[f"x={value[0]}, y={value[1]}" for value in _UNACCEPTABLE_DATA_FOR_TEST],
    )
    def test_unacceptable_values(self, x, y):
        """Тест проверяет недопустимые значения координат x, y (по типу данных)"""
        with pytest.raises((ValidationError, AssertionError)):
            assert self.vector(x, y)

    def test_acceptable_add_vector(self):
        """Тест проверяет успешную операцию сложения векторов"""
        vector_ = self.vector(1, 2) + self.vector(3, 4)
        with soft_assertions():
            assert vector_.x == 4
            assert vector_.y == 6

    def test_unacceptable_add_vector(self):
        """Тест проверяет неуспешную операцию сложения векторов"""
        with pytest.raises(AttributeError):
            self.vector(1, 2) + 5

    def test_acceptable_equals_vector(self):
        """Тест проверяет успешную операцию эквивалентности векторов"""
        assert self.vector(1, 1) == self.vector(1, 1)

    def test_unacceptable_equals_vector(self):
        """Тест проверяет неуспешную операцию эквивалентности векторов"""
        with pytest.raises(AssertionError):
            assert self.vector(1, 1) == self.vector(2, 1)

    def test_acceptable_more_vector(self):
        """Тест проверяет успешную операцию 'больше' векторов"""
        assert self.vector(1, 1) > self.vector(0, 0)

    def test_acceptable_less_vector(self):
        """Тест проверяет успешную операцию 'меньше' векторов"""
        assert self.vector(0, 0) < self.vector(1, 1)

    def test_valid_data_display(self):
        """Тест проверяет корректное отображение вектора на экране"""
        assert str(Vector(1, 2)) == "(1, 2)"
