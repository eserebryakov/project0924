class QuadraticEquation:
    @staticmethod
    def solve(a, b, c):
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return []
