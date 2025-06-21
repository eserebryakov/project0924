import threading
import time
from uuid import uuid4

import pytest

from src.spacebattle.commands.create_object import CreateObjectCommand
from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common import constants
from src.spacebattle.common.vector import Vector
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestInterpreter:
    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        InitCommand().execute()
        self.game_id = str(uuid4())
        self.object_id_1 = str(uuid4())
        self.object_id_2 = str(uuid4())
        self.object_1 = {
            "object_id": self.object_id_1,
            "location": Vector(2, 2).model_dump(),
            "velocity": Vector(0, 0).model_dump(),
        }
        self.object_2 = {
            "object_id": self.object_id_2,
            "location": Vector(5, 7).model_dump(),
            "velocity": Vector(0, 0).model_dump(),
        }
        CreateObjectCommand(game_id=self.game_id, object_id=self.object_id_1, obj=self.object_1).execute()
        CreateObjectCommand(game_id=self.game_id, object_id=self.object_id_2, obj=self.object_2).execute()
        self.start_command = StartCommand(game_id=self.game_id)
        self.start_command.execute()

        self.order_1 = {
            "action": constants.ACTION_HARD_STOP,
            "server": IoC.resolve(f"{constants.IOC_THREAD}.{self.game_id}"),
            "price": 10,
        }

        self.order_2 = {
            "action": constants.ACTION_MOVE,
            "game_id": self.game_id,
            "object_id": self.object_id_2,
            "velocity": Vector(5, 5).model_dump(),
        }

        def teardown():
            time.sleep(0.1)
            server = IoC.resolve(f"{constants.IOC_THREAD}.{self.game_id}")
            server.queue.put(HardStopCommand(server))
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_interpreter(self, initial_state):
        print(InitCommand.root_scope)
        print(IoC.resolve(constants.GAME_OBJECT, self.game_id, self.object_id_1))
        ...
        # interpreter_command = InterpreterCommand(order=self.order_1)
        # interpreter_command.execute()
        # interpreter_command = InterpreterCommand(order=self.order_2)
        # interpreter_command.execute()
