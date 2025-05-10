import pytest
from assertpy import soft_assertions

from src.spacebattle.commands.update_ioc_resolve_dependency_strategy import (
    UpdateIocResolveDependencyStrategyCommand,
)
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestUpdateIocResolveDependencyStrategyCommand:
    """Тест проверяющий команду, обновляющую стратегию"""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        IoC.strategy = _strategy
        self.upd_strategy = lambda x: x
        IoC.strategy = "test_strategy"
        self.update_ioc_resolve_dependency_strategy = UpdateIocResolveDependencyStrategyCommand(
            self.upd_strategy,
        )

        def teardown():
            IoC.strategy = _strategy

        request.addfinalizer(teardown)

    def test_update_ioc_resolve_dependency_strategy(self, initial_state):
        """П4. Тест проверяет команду, которая обновляет стратегию."""
        self.update_ioc_resolve_dependency_strategy.execute()
        with soft_assertions():
            assert IoC.strategy == "test_strategy"
            assert self.update_ioc_resolve_dependency_strategy._update_ioc_strategy is self.upd_strategy
