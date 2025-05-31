import threading
from uuid import uuid4

import pytest

from src.spacebattle.commands.create_object import CreateObjectCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.common import constants
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestCreateObjectCommand:
    """Тест проверяет работу команды по созданию объекта в игре"""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        self.game_id = str(uuid4())
        self.object_id = str(uuid4())
        self.object = {"value": 1}
        self.command = CreateObjectCommand(game_id=self.game_id, object_id=self.object_id, obj=self.object)

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_create_object(self, initial_state):
        InitCommand().execute()
        self.command.execute()
        assert IoC.resolve(constants.GAME_OBJECT, self.game_id, self.object_id) == self.object
