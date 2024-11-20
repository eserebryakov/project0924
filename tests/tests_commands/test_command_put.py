from queue import Queue

import pytest

from src.spacebattle.commands import Command, PutCommand


class MockCommand(Command):
    def execute(self):
        ...


class TestPutCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.command = MockCommand()
        self.queue = Queue()
        self.put_command = PutCommand(self.command, self.queue)

    def test_put_command(self):
        """Тест проверяет команду которая, кладет в очередь любую команду"""
        self.put_command.execute()
        assert self.queue.get() == self.command
