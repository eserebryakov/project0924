from queue import Queue

import pytest

from src.spacebattle.commands import Command, RetryCommand


class MockCommand(Command):
    def __init__(self, queue: Queue):
        self.queue = queue

    def execute(self):
        self.queue.put(self)


class TestRetryCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.queue = Queue()
        self.command = MockCommand(queue=self.queue)
        self.retry_command = RetryCommand(self.command)

    def test_retry_command(self):
        """Тест проверяет команду которая, повторяет другую команду"""
        self.retry_command.execute()
        assert self.queue.get() == self.command
