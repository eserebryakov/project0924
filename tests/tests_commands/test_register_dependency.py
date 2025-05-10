import threading

import pytest

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.register_dependency import RegisterDependencyCommand
from src.spacebattle.common.constants import IOC_SCOPE_CURRENT
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy

IOC_TEST_DEPENDENCY = "IoC.Test.Dependency"


class TestRegisterDependencyCommand:
    """Тест проверяющий команду, регистрирующую зависимость."""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        self.register_dependency = RegisterDependencyCommand(
            dependency=IOC_TEST_DEPENDENCY, strategy=lambda: "TestStrategy"
        )

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_register_dependency(self, initial_state):
        """П4. Тест проверяет команду, которая регистрирует зависимость."""
        InitCommand().execute()
        self.register_dependency.execute()
        assert IoC.resolve(IOC_SCOPE_CURRENT)[IOC_TEST_DEPENDENCY]() == "TestStrategy"
