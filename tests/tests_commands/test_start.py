import threading
from uuid import uuid4

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common import constants
from src.spacebattle.core.commands_mapping import COMMANDS
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestStartCommand:
    """Тест проверяет команду стартующую код сервера в отдельном потоке"""

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
        self.command = StartCommand(game_id=self.game_id)

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_start_command(self, initial_state):
        self.command.execute()
        server = IoC.resolve(f"{constants.IOC_THREAD}.{self.game_id}")
        with soft_assertions():
            assert f"{constants.IOC_THREAD}.{self.game_id}" in InitCommand.root_scope
            assert f"{constants.IOC_QUEUE}.{self.game_id}" in InitCommand.root_scope
            assert constants.ADAPTER in InitCommand.root_scope
            assert server.is_running
        server.queue.put(HardStopCommand(server))

    @pytest.mark.parametrize("command_names", COMMANDS.keys())
    def test_start_commands_mapping(self, initial_state, command_names):
        self.command.execute()
        server = IoC.resolve(f"{constants.IOC_THREAD}.{self.game_id}")
        assert command_names in InitCommand.root_scope
        server.queue.put(HardStopCommand(server))
