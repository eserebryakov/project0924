from queue import Queue

import pytest

from src.spacebattle.commands import Command, Retry2Command


class MockCommand(Command):
    def __init__(self, queue: Queue):
        self.queue = queue

    def execute(self):
        self.queue.put(self)


class TestRetry2Command:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.queue = Queue()
        self.command = MockCommand(queue=self.queue)
        self.retry2_command = Retry2Command(self.command)

    def test_retry2_command(self):
        """Тест проверяет команду которая, повторяет другую команду"""
        self.retry2_command.execute()
        assert self.queue.get() == self.command
