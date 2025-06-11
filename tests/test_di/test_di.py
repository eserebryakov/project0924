import threading
import time
from uuid import uuid4

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands.handle_exception import HandleExceptionCommand
from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common import Fuel, Vector, constants
from src.spacebattle.core.dependencies import spaceship_move
from src.spacebattle.objects.burning import BurningObject
from src.spacebattle.objects.moving import MovingObject
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class ValidObject(MovingObject, BurningObject):
    def __init__(self):
        self.__location = Vector(0, 0)
        self.__velocity = Vector(7, 7)
        self.__fuel = Fuel(10)
        self.__fuel_velocity = Fuel(3)

    def get_location(self) -> Vector:
        return self.__location

    def set_location(self, value: Vector) -> None:
        self.__location = value

    def get_velocity(self) -> Vector:
        return self.__velocity

    def get_fuel(self) -> Fuel:
        return self.__fuel

    def set_fuel(self, value: Fuel) -> None:
        self.__fuel = value

    def get_fuel_velocity(self) -> Fuel:
        return self.__fuel_velocity


class TestDi:
    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        InitCommand().execute()
        self.valid_object = ValidObject()
        self.game_id = uuid4()
        self.command = StartCommand(game_id=self.game_id)
        self.command.execute()
        server = IoC.resolve(f"{constants.IOC_THREAD}.{self.game_id}")
        IoC.resolve(
            constants.IOC_REGISTER,
            constants.RULE_SPACESHIP_MOVE,
            lambda: [constants.COMMAND_CHECK_FUEL, constants.COMMAND_MOVING_STRAIGHT_LINE, constants.COMMAND_BURN_FUEL],
        ).execute()
        IoC.resolve(
            constants.IOC_REGISTER,
            constants.SPACESHIP_MOVE,
            lambda *args, queue_=server.queue: spaceship_move(*args, queue=queue_),
        ).execute()
        IoC.resolve(
            constants.IOC_REGISTER, constants.IOC_HANDLE_EXCEPTION, lambda c_, e_: HandleExceptionCommand(c_, e_)
        ).execute()

        yield

        time.sleep(0.1)
        server = IoC.resolve(f"{constants.IOC_THREAD}.{self.game_id}")
        server.queue.put(HardStopCommand(server))
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

    def test_di(self, initial_state):
        server = IoC.resolve(f"{constants.IOC_THREAD}.{self.game_id}")
        command = IoC.resolve(constants.SPACESHIP_MOVE, self.valid_object)
        server.queue.put(command)
        time.sleep(0.1)
        with soft_assertions():
            assert self.valid_object.get_location() == Vector(21, 21)
            assert self.valid_object.get_fuel() == Fuel(1)
