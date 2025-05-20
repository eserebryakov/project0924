import threading
from abc import ABC, abstractmethod

import pytest

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.set_attribute_value import SetAttributeValueCommand
from src.spacebattle.common.constants import ADAPTER, IOC_REGISTER
from src.spacebattle.scopes.adapter import auto_generate_adapter
from src.spacebattle.scopes.default_get_property_strategy import (
    DefaultGetPropertyStrategy,
)
from src.spacebattle.scopes.default_set_property_strategy import (
    DefaultSetPropertyStrategy,
)
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class MockObject(ABC):
    @abstractmethod
    def get_value(self):
        ...

    @abstractmethod
    def set_value(self, value):
        ...

    @abstractmethod
    def any_method(self):
        ...


MOCK_OBJECT = {
    "value": 5,
}


class TestMockObjectAdapter:
    """Тест проверяющий работу автоматический генерации адаптера."""

    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        InitCommand().execute()
        IoC.resolve(IOC_REGISTER, ADAPTER, lambda class_, obj: auto_generate_adapter(class_, obj)).execute()

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    @pytest.fixture(scope="function")
    def mock_object_adapter(self, initial_state):
        return IoC.resolve(ADAPTER, MockObject, MOCK_OBJECT)

    @pytest.fixture(scope="function")
    def register_mock_object_attributes(self, mock_object_adapter):
        IoC.resolve(
            IOC_REGISTER,
            f"{MockObject.__name__}.value.get",
            lambda obj: DefaultGetPropertyStrategy(obj=obj.obj, attribute="value").resolve(),
        ).execute()
        IoC.resolve(
            IOC_REGISTER,
            f"{MockObject.__name__}.value.set",
            lambda obj, attribute, value: SetAttributeValueCommand(
                obj=obj.obj, attribute=attribute, value=value, strategy=DefaultSetPropertyStrategy
            ),
        ).execute()

    def test_any_method(self, mock_object_adapter):
        assert isinstance(type(mock_object_adapter.any_method), type(classmethod))

    @pytest.mark.parametrize("attribute", ["get_value", "set_value", "obj", "any_method"])
    def test_available_attributes(self, mock_object_adapter, attribute, register_mock_object_attributes):
        assert getattr(mock_object_adapter, attribute)

    def test_unavailable_attributes(self, mock_object_adapter, register_mock_object_attributes):
        with pytest.raises(AttributeError):
            assert getattr(mock_object_adapter, "unavailable_attributes")

    def test_mock_object_adapter(self, mock_object_adapter, register_mock_object_attributes):
        mock_object_adapter.set_value(10)
        assert mock_object_adapter.get_value() == 10
