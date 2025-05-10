import threading

import pytest

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.register_dependency import RegisterDependencyCommand
from src.spacebattle.common.constants import IOC_SCOPE_CURRENT
from src.spacebattle.scopes.ioc import IoC

IOC_TEST_DEPENDENCY = "IoC.Test.Dependency"


class TestRegisterDependencyCommand:
    """Тест проверяющий команду, регистрирующую зависимость."""

    @pytest.fixture(scope="function")
    def original_dependencies(self, request):
        print(InitCommand.root_scope)
        print(InitCommand.current_scope)
        print(InitCommand.already_executed_successfully)
        print(IoC.strategy)
        InitCommand().execute()
        self.register_dependency = RegisterDependencyCommand(
            dependency=IOC_TEST_DEPENDENCY, strategy=lambda: "TestStrategy"
        )

        def teardown():
            # del IoC.resolve(IOC_SCOPE_CURRENT)[IOC_TEST_DEPENDENCY]
            InitCommand.root_scope = dict()
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False

        request.addfinalizer(teardown)

    def test_register_dependency(self, original_dependencies):
        """П4. Тест проверяет команду, которая регистрирует зависимость."""
        self.register_dependency.execute()
        assert IoC.resolve(IOC_SCOPE_CURRENT)[IOC_TEST_DEPENDENCY]() == "TestStrategy"
