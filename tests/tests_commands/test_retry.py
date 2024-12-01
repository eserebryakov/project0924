from queue import Queue

import pytest

from src.spacebattle.commands import Command, Retry2Command, RetryCommand


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

    @pytest.mark.parametrize("command", [RetryCommand, Retry2Command])
    def test_retry_command(self, command):
        """Тест проверяет команду которая, повторяет другую команду"""
        command(self.command).execute()
        assert self.queue.get() == self.command
