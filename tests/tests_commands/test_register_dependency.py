import pytest

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.register_dependency import RegisterDependencyCommand
from src.spacebattle.common.constants import IOC_SCOPE_CURRENT
from src.spacebattle.scopes.ioc import IoC

IOC_TEST_DEPENDENCY = "IoC.Test.Dependency"


class TestRegisterDependencyCommand:
    """Тест проверяющий команду, регистрирующую зависимость."""

    @pytest.fixture(autouse=True)
    def setup(self):
        InitCommand().execute()
        self.register_dependency = RegisterDependencyCommand(
            dependency=IOC_TEST_DEPENDENCY, strategy=lambda: "TestStrategy"
        )

    def test_register_dependency(self):
        """П4. Тест проверяет команду, которая регистрирует зависимость."""
        self.register_dependency.execute()
        assert IoC.resolve(IOC_SCOPE_CURRENT)[IOC_TEST_DEPENDENCY]() == "TestStrategy"
