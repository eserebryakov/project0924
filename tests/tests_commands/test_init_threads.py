import threading

import pytest

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.common import constants
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestInitCommand:
    """Тест проверяет работу команды INIT в потоках (threads)"""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_init_command_same_root_scope(self, initial_state):
        """П5. Тест проверяет, что потоки получают одинаковый root_scope"""
        init_threads = []
        root_scopes_values = []

        def thread_function():
            init_command = InitCommand()
            init_command.execute()
            scope = IoC.resolve(constants.IOC_SCOPE_CREATE)
            IoC.resolve(constants.IOC_SCOPE_CURRENT_SET, scope).execute()
            root_scope = IoC.resolve(constants.IOC_SCOPE_CURRENT).__getitem__(constants.IOC_SCOPE_PARENT)()
            root_scopes_values.append(root_scope)

        for _ in range(5):
            thread = threading.Thread(target=thread_function)
            init_threads.append(thread)
            thread.start()

        for thread in init_threads:
            thread.join()

        first_scope = root_scopes_values[0]
        for r_scope in root_scopes_values:
            assert r_scope == first_scope

    def test_init_command_unique_current_scope(self, initial_state):
        """П5. Тест проверяет, что потоки получают уникальные current_scope"""
        init_threads = []
        current_scopes_values = []

        def thread_function():
            init_command = InitCommand()
            init_command.execute()
            IoC.resolve(constants.IOC_SCOPE_CURRENT_SET, lambda: 1).execute()
            current_scopes_values.append(init_command.current_scope.value)

        for _ in range(5):
            thread = threading.Thread(target=thread_function)
            init_threads.append(thread)
            thread.start()

        for thread in init_threads:
            thread.join()

        assert len(set(current_scopes_values)) == 5

    def test_init_command_should_execute_only_once(self, initial_state):
        """П5. Тест проверяет, выполняется только один раз для всех потоков"""

        def execute_init():
            InitCommand().execute()

        init_threads = []
        for _ in range(5):
            thread = threading.Thread(target=execute_init)
            init_threads.append(thread)
            thread.start()

        for thread in init_threads:
            thread.join()

        assert InitCommand.already_executed_successfully
