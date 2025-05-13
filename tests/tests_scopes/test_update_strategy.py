import pytest

from src.spacebattle.common.constants import UPDATE_IOC_RESOLVE_DEPENDENCY_STRATEGY
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestUpdateStrategy:
    """Тест проверяющий работу стратегии."""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        IoC.strategy = _strategy
        self.strategy = _strategy

        def teardown():
            IoC.strategy = _strategy

        request.addfinalizer(teardown)

    def test_successful_update_strategy(self, initial_state):
        self.strategy(UPDATE_IOC_RESOLVE_DEPENDENCY_STRATEGY, lambda _: "test_strategy").execute()
        assert IoC.strategy == "test_strategy"

    def test_unsuccessful_update_strategy(self, initial_state):
        """Тест проверяющий неуспешное обновление стратегии."""
        with pytest.raises(KeyError):
            self.strategy("UNAVAILABLE_KEY")
