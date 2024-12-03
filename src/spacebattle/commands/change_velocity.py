import logging
import math

from src.spacebattle.common import Angle, Vector

from . import Command


class ChangeVelocityCommand(Command):
    def __init__(self, vector: Vector, angle: Angle) -> None:
        self.vector = vector
        self.angle = angle
        self.log = logging.getLogger(__name__)

    def execute(self):
        velocity = math.sqrt(self.vector.x**2 + self.vector.y**2)
        x_ = int(velocity * math.cos(math.radians(self.angle.d * (360 / self.angle.n))))
        y_ = int(velocity * math.sin(math.radians(self.angle.d * (360 / self.angle.n))))
        self.log.debug(f"Меняем вектор мгновенной скорости с {self.vector} на {Vector(x_, y_)}")
        self.vector.x = x_
        self.vector.y = y_
