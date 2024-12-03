import pytest

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.write import WriteCommand


class MockCommand(Command):
    def execute(self):
        ...


class TestWriteCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.command = MockCommand()
        self.exception = Exception("TestWriteCommandException")
        self.write_command = WriteCommand(self.command, self.exception)

    def test_write_command(self):
        """Тест проверяет команду которая, логирует другую команду"""
        self.write_command.execute()
