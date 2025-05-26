import threading

import pytest

from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common.constants import IOC_THREAD
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
        self.command = StartCommand()

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
        server = IoC.resolve(IOC_THREAD)
        assert server.is_running
        server.queue.put(HardStopCommand(server))
