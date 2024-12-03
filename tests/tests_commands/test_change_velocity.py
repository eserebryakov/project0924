import pytest

<<<<<<< HEAD
from src.spacebattle.commands.change_velocity import ChangeVelocityCommand
=======
from src.spacebattle.commands import ChangeVelocityCommand
>>>>>>> d8de736 (DZ3: Добавил домашнее задание по теме Команда)
from src.spacebattle.common import Angle, Vector


class TestChangeVelocityCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
<<<<<<< HEAD
        self.velocity = Vector(110, 326)
=======
        self.velocity = Vector(0, 0)
>>>>>>> d8de736 (DZ3: Добавил домашнее задание по теме Команда)
        self.angle = Angle(3, 16)
        self.command = ChangeVelocityCommand(self.velocity, self.angle)

    def test_change_velocity(self):
        self.command.execute()
<<<<<<< HEAD
        assert self.velocity == Vector(131, 317)
=======
        assert self.velocity == Vector(151, 366)
>>>>>>> d8de736 (DZ3: Добавил домашнее задание по теме Команда)
