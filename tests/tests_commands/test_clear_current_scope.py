import threading

import pytest

from src.spacebattle.commands.clear_current_scope import ClearCurrentScopeCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestClearCurrentScopeCommand:
    """Тест проверяющий команду, очищающую текущий scope."""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        InitCommand.current_scope.value = 1
        self.clear_command = ClearCurrentScopeCommand()

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_clear_current_scope(self, initial_state):
        """П4. Тест проверяет команду, которая очищает текущий scope."""
        self.clear_command.execute()
        with pytest.raises(AttributeError):
            assert InitCommand.current_scope.value
