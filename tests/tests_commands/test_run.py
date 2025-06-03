import threading
import time
from queue import Queue

import pytest

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.run import RunCommand
from src.spacebattle.common import constants
from src.spacebattle.core.server import ServerThread
from src.spacebattle.core.state import Context, NormalState
from src.spacebattle.exceptions.exception_handler import (
    ExceptionHandler,
    exception_handler_put_command,
)
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class MockException(Exception):
    ...


class MockCommand(Command):
    def execute(self):
        raise MockException("MockException")


class TestRunCommand:
    """Тест проверяет работу команды RunCommand"""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        InitCommand().execute()
        IoC.resolve(
            constants.IOC_REGISTER,
            constants.IOC_HANDLE_EXCEPTION,
            lambda command, e: ExceptionHandler.handle(command, e).execute(),
        ).execute()
        self.queue = Queue()
        self.new_queue = Queue()
        self.server = ServerThread(self.queue)
        self.context = Context()
        self.run_command = RunCommand(
            server=self.server,
            context=self.context,
        )

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

    def test_run_command(self, initial_state):
        self.run_command.execute()
        assert isinstance(self.context.state, NormalState)

    def test_run_command_exception(self, initial_state):
        exception_handler_put_command(command=MockCommand(), exception=MockException(), queue=self.new_queue)
        self.run_command.execute()
        self.server.start()
        self.queue.put(MockCommand())
        time.sleep(0.1)
        assert self.new_queue.qsize() == 1
