import pytest

from src.spacebattle.commands.change_velocity import ChangeVelocityCommand
from src.spacebattle.common import Angle, Vector


class TestChangeVelocityCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.velocity = Vector(110, 326)
        self.angle = Angle(3, 16)
        self.command = ChangeVelocityCommand(self.velocity, self.angle)

    def test_change_velocity(self):
        self.command.execute()
        assert self.velocity == Vector(131, 317)
