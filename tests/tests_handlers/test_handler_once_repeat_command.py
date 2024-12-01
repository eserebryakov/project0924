import logging
from queue import Queue

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands import Command, RetryCommand, WriteCommand
from src.spacebattle.exceptions.exception_handler import (
    ExceptionHandler,
    exception_handler_once_repeat_command,
)


class MockException(Exception):
    ...


class MockCommand(Command):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def execute(self):
        exception = MockException("MockException")
        self.log.debug(f"Выполнили команду {self} и вызвали исключение {exception}")
        raise exception


class TestHandlerOnceRepeatCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.command = MockCommand()
        self.exception = MockException("MockException")
        self.queue = Queue()

    def test_handle_once_repeat_command(self):
        """Тест проверяет что при первом выбросе исключения повторить команду,
        при повторном выбросе исключения записать информацию в лог."""
        exception_handler_once_repeat_command(command=self.command, exception=self.exception, queue=self.queue)
        try:
            self.command.execute()
        except MockException as exception:
            ExceptionHandler.handle(command=self.command, exception=exception).execute()

        retry_command = self.queue.get()
        try:
            retry_command.execute()
        except MockException as exception:
            ExceptionHandler.handle(command=retry_command, exception=exception).execute()

        write_command = self.queue.get()
        write_command.execute()

        with soft_assertions():
            assert isinstance(retry_command, RetryCommand)
            assert isinstance(write_command, WriteCommand)
            assert self.queue.qsize() == 0
