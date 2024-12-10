import pytest

from src.spacebattle.commands.change_velocity import ChangeVelocityCommand
from src.spacebattle.common import Angle, Vector


class TestChangeVelocityCommand:
    """Тест проверяющий команду изменяющую вектор мгновенной скорости в зависимости от угла"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.velocity = Vector(39, 734)
        self.angle = Angle(2, 64)
        self.command = ChangeVelocityCommand(self.velocity, self.angle)

    def test_change_velocity(self):
        """П9 Тест проверяет что вектор мгновенной скорости меняется в зависимости от угла"""
        self.command.execute()
        assert self.velocity == Vector(720, 143)
