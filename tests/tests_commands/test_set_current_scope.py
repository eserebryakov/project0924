import threading

import pytest

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.set_current_scope import SetCurrentScopeCommand
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestSetCurrentScopeCommand:
    """Тест проверяющий команду, устанавливающую текущий scope."""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        self.set_command = SetCurrentScopeCommand(scope="test_scope")

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_set_current_scope(self, initial_state):
        """П4. Тест проверяет команду, которая устанавливает текущий scope."""
        self.set_command.execute()
        assert InitCommand.current_scope.value == "test_scope"
