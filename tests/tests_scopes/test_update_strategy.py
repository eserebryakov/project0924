import pytest

from src.spacebattle.common.constants import UPDATE_IOC_RESOLVE_DEPENDENCY_STRATEGY
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestUpdateStrategy:
    """Тест проверяющий работу стратегии."""

    @pytest.fixture(scope="function")
    def strategy(self, request):
        self.strategy = _strategy

        def teardown():
            IoC.strategy = _strategy

        request.addfinalizer(teardown)

    def test_successful_update_strategy(self, strategy):
        self.strategy(UPDATE_IOC_RESOLVE_DEPENDENCY_STRATEGY, lambda _: "test_strategy").execute()
        assert IoC.strategy == "test_strategy"

    def test_unsuccessful_update_strategy(self, strategy):
        """Тест проверяющий неуспешное обновление стратегии."""
        with pytest.raises(KeyError):
            self.strategy("UNAVAILABLE_KEY")
