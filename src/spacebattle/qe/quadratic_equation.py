import cmath

from assertpy import soft_assertions

from src.spacebattle.exceptions.exeptions import ZeroValueError


class QuadraticEquation:
    @staticmethod
    def solve(a, b, c, e=1e-5):
        with soft_assertions():
            assert type(a) in [int, float]
            assert type(b) in [int, float]
            assert type(c) in [int, float]
            assert type(e) in [int, float]

        if abs(a) <= e:
            raise ZeroValueError("a не должно быть равно 0")
        discriminant = b * b - 4 * a * c

        if discriminant < -e:
            return []

        if abs(discriminant) <= e:
            return -b / (2 * a), -b / (2 * a)

        if discriminant > e:
            return -b + cmath.sqrt(discriminant) / 2.0 / a, -b - cmath.sqrt(discriminant) / 2.0 / a
