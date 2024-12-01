from queue import Queue

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands import Command, WriteCommand
from src.spacebattle.exceptions.exception_handler import (
    ExceptionHandler,
    exception_handler_put_command,
    exception_handler_put_write_command,
)


class MockException(Exception):
    ...


class MockCommand(Command):
    def execute(self):
        raise MockException("Test Exception")


class TestHandlerPutCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.command = MockCommand()
        self.exception = MockException("MockException")
        self.queue = Queue()

    def test_handler_put_any_command(self):
        """Тест проверяет обработчик исключения, который ставит любую Команду в очередь Команд."""
        exception_handler_put_command(command=self.command, exception=self.exception, queue=self.queue)
        try:
            self.command.execute()
        except Exception as exception:
            ExceptionHandler.handle(command=self.command, exception=exception).execute()
        with soft_assertions():
            assert self.queue.get() == self.command
            assert self.queue.qsize() == 0

    def test_handler_put_write_command(self):
        """Тест проверят обработчик исключения, который ставит Команду, пишущую в лог в очередь Команд."""
        exception_handler_put_write_command(command=self.command, exception=self.exception, queue=self.queue)
        ExceptionHandler.handle(command=self.command, exception=self.exception).execute()
        with soft_assertions():
            assert isinstance(self.queue.get(), WriteCommand)
            assert self.queue.qsize() == 0
