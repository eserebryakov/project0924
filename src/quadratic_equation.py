import cmath


class QuadraticEquation:
    @staticmethod
    def solve(a, b, c):
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return []

        if discriminant > 0:
            return -b + cmath.sqrt(discriminant) / 2.0 / a, -b - cmath.sqrt(discriminant) / 2.0 / a
