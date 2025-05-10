import pytest

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.set_current_scope import SetCurrentScopeCommand


class TestSetCurrentScopeCommand:
    """Тест проверяющий команду, устанавливающую текущий scope."""

    @pytest.fixture(scope="function")
    def original_scope(self, request):
        current_scope = InitCommand.current_scope
        self.set_command = SetCurrentScopeCommand(scope="test_scope")

        def teardown():
            InitCommand.current_scope = current_scope

        request.addfinalizer(teardown)

    def test_set_current_scope(self, original_scope):
        """П4. Тест проверяет команду, которая устанавливает текущий scope."""
        self.set_command.execute()
        assert InitCommand.current_scope.value == "test_scope"
