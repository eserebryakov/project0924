import logging

import pytest

from src.spacebattle.commands import Command, WriteCommand
from src.spacebattle.exception_handler import ExceptionHandler


class MockException(Exception):
    ...


class MockCommand(Command):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def execute(self):
        exception = MockException("MockException")
        self.log.debug(f"Выполнили команду {self} и вызвали исключение {exception}")
        raise exception


class TestHandlerMissingCommandsAndExceptions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.command = MockCommand()
        self.exception = MockException("MockException")

    def test_handler_missing_command(self):
        """Тест проверяет что команда, отсутствующая в обработчике, обрабатывается default командой"""
        with pytest.raises(MockException):
            ExceptionHandler.handle(command=self.command, exception=self.exception).execute()

    def test_handler_missing_exception(self):
        """Тест проверяет что исключение, отсутствующее в обработчике, обрабатывается default командой"""
        ExceptionHandler.register_handler(
            command_type=type(self.command),
            exception_type=type(AssertionError),
            handler=lambda c, e: WriteCommand(command=c, exception=e),
        )
        with pytest.raises(MockException):
            ExceptionHandler.handle(command=self.command, exception=self.exception).execute()
