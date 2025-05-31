import itertools
import sys

import pytest
from assertpy import soft_assertions
from pydantic import ValidationError

from src.spacebattle.common.angle import Angle

# Допустимые значения типов данных (позитивный тест)
_ACCEPTABLE_VALUES = (sys.maxsize, -sys.maxsize - 1, -1, 0, 1)
_LIST_ACCEPTABLE_VALUES = (_ACCEPTABLE_VALUES, _ACCEPTABLE_VALUES)
_ACCEPTABLE_DATA_FOR_TEST = [val for val in list(itertools.product(*_LIST_ACCEPTABLE_VALUES)) if val[0] < val[1]]

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


class TestAngle:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.angle = Angle

    @pytest.mark.parametrize(
        "x, y", _ACCEPTABLE_DATA_FOR_TEST, ids=[f"x={value[0]}, y={value[1]}" for value in _ACCEPTABLE_DATA_FOR_TEST]
    )
    def test_acceptable_values(self, x, y):
        """Тест проверяет допустимые граничные значения угла d, n: max, min, -1, 0 1"""
        assert self.angle(x, y)

    @pytest.mark.parametrize(
        "x, y",
        _UNACCEPTABLE_DATA_FOR_TEST,
        ids=[f"x={value[0]}, y={value[1]}" for value in _UNACCEPTABLE_DATA_FOR_TEST],
    )
    def test_unacceptable_values(self, x, y):
        """Тест проверяет недопустимые значения угла d, n (по типу данных)"""
        with pytest.raises((ValidationError, AssertionError)):
            assert self.angle(x, y)

    def test_direction_is_greater_than_or_equals_number_of_parts(self):
        """Тест проверяет что создание угла с направлением больше (либо равно) чем кол-ва частей приводит к ошибке"""
        with pytest.raises(AssertionError):
            assert self.angle(2, 1)
            assert self.angle(1, 1)

    def test_acceptable_add_angle(self):
        """Тест проверяет успешную операцию сложения векторов"""
        angle_ = self.angle(1, 7) + self.angle(3, 7)
        with soft_assertions():
            assert angle_ == Angle(4, 7)

    def test_unacceptable_add_angle(self):
        """Тест проверяет неуспешную операцию сложения векторов"""
        with pytest.raises(AttributeError):
            self.angle(1, 2) + 5

    def test_unacceptable_add_angle_different_parts(self):
        """Тест проверяет неуспешную операцию сложения векторов если n разное"""
        with pytest.raises(AssertionError):
            self.angle(1, 2) + self.angle(1, 3)

    def test_acceptable_equals_angle(self):
        """Тест проверяет успешную операцию эквивалентности векторов"""
        assert self.angle(1, 3) == self.angle(1, 3)

    def test_unacceptable_equals_angle(self):
        """Тест проверяет неуспешную операцию эквивалентности векторов"""
        with pytest.raises(AssertionError):
            assert self.angle(1, 3) == self.angle(2, 3)

    def test_valid_data_display(self):
        """Тест проверяет корректное отображение угла на экране"""
        assert str(Angle(1, 2)) == "(1, 2)"
