import threading
import time
from uuid import uuid4

import pytest

from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common import constants
from src.spacebattle.common.vector import Vector
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy

_object_id = str(uuid4())

TEST_OBJECT = {
    "object_id": _object_id,
    "location": Vector(2, 2).model_dump(),
    "velocity": Vector(0, 0).model_dump(),
}

ORDER = {"object_id": _object_id, "action": "StartMove", "velocity": Vector(5, 5).model_dump()}


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
        self.game_id = uuid4()
        self.start_command = StartCommand(game_id=self.game_id)
        self.start_command.execute()

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
        ...
