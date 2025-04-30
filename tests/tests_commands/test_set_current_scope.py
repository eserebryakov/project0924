import pytest

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.set_current_scope import SetCurrentScopeCommand


class TestSetCurrentScopeCommand:
    """Тест проверяющий команду, устанавливающую текущий scope."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.set_command = SetCurrentScopeCommand(scope="test_scope")

    def test_clear_current_scope(self):
        """П4. Тест проверяет команду, которая устанавливает текущий scope."""
        self.set_command.execute()
        assert InitCommand.current_scope.value == "test_scope"
