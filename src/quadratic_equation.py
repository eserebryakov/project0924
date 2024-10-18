import cmath

from src.exeptions import ZeroValueError


class QuadraticEquation:
    @staticmethod
    def solve(a, b, c, e=1e-5):
        if abs(a) <= e:
            raise ZeroValueError("a не должно быть равно 0")
        discriminant = b * b - 4 * a * c

        if discriminant < -e:
            return []

        if abs(discriminant) <= e:
            return -b / (2 * a), -b / (2 * a)

        if discriminant > e:
            return -b + cmath.sqrt(discriminant) / 2.0 / a, -b - cmath.sqrt(discriminant) / 2.0 / a
