import threading
import time
from queue import Queue

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.handle_exception import HandleExceptionCommand
from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.common.constants import IOC_HANDLE_EXCEPTION, IOC_REGISTER
from src.spacebattle.core.server import ServerThread
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class MockException(Exception):
    ...


class MockCommand(Command):
    def execute(self):
        raise MockException("MockException")


class TestHardStopCommand:
    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        InitCommand().execute()
        IoC.resolve(IOC_REGISTER, IOC_HANDLE_EXCEPTION, lambda c_, e_: HandleExceptionCommand(c_, e_)).execute()
        self.queue_ = Queue()
        self.server = ServerThread(queue=self.queue_)
        self.command = HardStopCommand(server=self.server)
        self.queue_.put(MockCommand())
        self.queue_.put(MockCommand())
        self.queue_.put(self.command)
        self.queue_.put(MockCommand())
        self.queue_.put(MockCommand())

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_hard_stop(self, initial_state):
        self.server.start()
        time.sleep(0.1)
        with soft_assertions():
            assert not self.server.is_running
            assert self.queue_.qsize() == 2
