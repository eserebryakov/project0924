import pytest

from src.spacebattle.commands.clear_current_scope import ClearCurrentScopeCommand
from src.spacebattle.commands.init import InitCommand


class TestClearCurrentScopeCommand:
    """Тест проверяющий команду, очищающую текущий scope."""

    @pytest.fixture(scope="function")
    def original_scope(self, request):
        current_scope = InitCommand.current_scope
        InitCommand.current_scope.value = 1
        self.clear_command = ClearCurrentScopeCommand()

        def teardown():
            InitCommand.current_scope = current_scope

        request.addfinalizer(teardown)

    def test_clear_current_scope(self, original_scope):
        """П4. Тест проверяет команду, которая очищает текущий scope."""
        self.clear_command.execute()
        with pytest.raises(AttributeError):
            assert InitCommand.current_scope.value
