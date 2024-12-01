from queue import Queue

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands import Command, RetryCommand
from src.spacebattle.exceptions.exception_handler import (
    ExceptionHandler,
    exception_handler_put_repeater_command,
)


class MockException(Exception):
    ...


class MockCommand(Command):
    def execute(self):
        raise MockException("Test Exception")


class TestHandlerPutRepeaterCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.command = MockCommand()
        self.exception = MockException("MockException")
        self.queue = Queue()

    def test_handler_put_repeater_command(self):
        """Тест проверяет что при первом выбросе исключения повторить команду,
        при повторном выбросе исключения записать информацию в лог."""
        exception_handler_put_repeater_command(command=self.command, exception=self.exception, queue=self.queue)
        ExceptionHandler.handle(command=self.command, exception=self.exception).execute()
        with soft_assertions():
            assert isinstance(self.queue.get(), RetryCommand)
            assert self.queue.qsize() == 0
