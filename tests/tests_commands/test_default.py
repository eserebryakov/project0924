import pytest

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.default import DefaultCommand


class MockCommand(Command):
    def execute(self):
        ...


class MockException(Exception):
    ...


class TestDefaultCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.command = MockCommand()
        self.exception = MockException("TestDefaultCommandException")
        self.default_command = DefaultCommand(command=self.command, exception=self.exception)

    def test_default_command(self):
        """Тест проверяет команду по умолчанию"""
        with pytest.raises(MockException):
            self.default_command.execute()
