import threading
import time
from queue import Queue
from uuid import uuid4

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.move_to import MoveToCommand
from src.spacebattle.commands.put import PutCommand
from src.spacebattle.commands.run import RunCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common import constants
from src.spacebattle.core.state import Context
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class MockCommand(Command):
    def execute(self):
        ...


_NEW_QUEUE = "New.Queue"


class TestState:
    """Тест проверяет возможность смены режима обработки Команд в потоке, начиная со следующей Команды"""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        InitCommand().execute()
        self.game_id = uuid4()
        self.start_command = StartCommand(game_id=self.game_id)
        self.start_command.execute()

        self.server = IoC.resolve(f"{constants.IOC_THREAD}.{self.game_id}")
        self.queue = IoC.resolve(f"{constants.IOC_QUEUE}.{self.game_id}")
        IoC.resolve(constants.IOC_REGISTER, _NEW_QUEUE, lambda: Queue()).execute()
        self.new_queue = IoC.resolve(_NEW_QUEUE)

        self.context = Context()

        self.move_to_command = MoveToCommand(self.server, self.context, self.new_queue)
        self.hard_stop_command = HardStopCommand(self.server)
        self.run_command = RunCommand(self.server, self.context)
        self.put_command = PutCommand(MockCommand(), self.new_queue)

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value
            if self.server.is_running:
                self.server.stop()

        request.addfinalizer(teardown)

    def test_hard_stop_move_state(self, initial_state):
        """Тест проверяет, что в режиме Move To после команды hard stop, поток завершается"""
        self.queue.put(self.move_to_command)
        self.queue.put(self.hard_stop_command)
        time.sleep(0.1)
        with soft_assertions():
            assert not self.server.is_running
            assert self.queue.qsize() == 0

    def test_hard_stop_normal_state(self, initial_state):
        """Тест проверяет, что в режиме Normal после команды hard stop, поток завершается"""
        self.queue.put(self.run_command)
        self.queue.put(self.hard_stop_command)
        time.sleep(0.1)
        with soft_assertions():
            assert not self.server.is_running
            assert self.queue.qsize() == 0

    def test_state_move_to(self, initial_state):
        """Тест проверяет, что после команды MoveToCommand, поток переходит на обработку Команд с помощью состояния MoveTo"""
        self.queue.put(self.run_command)
        self.queue.put(self.move_to_command)
        self.queue.put(MockCommand())
        self.queue.put(self.hard_stop_command)
        time.sleep(0.1)
        assert self.new_queue.qsize() == 1

    def test_state_normal(self, initial_state):
        """Тест проверяет, что после команды RunCommand, поток переходит на обработку Команд с помощью состояния "Обычное"""
        self.queue.put(self.move_to_command)
        self.queue.put(self.run_command)
        self.queue.put(self.put_command)
        self.queue.put(self.hard_stop_command)
        time.sleep(0.1)
        assert self.new_queue.qsize() == 1
