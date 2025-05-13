import threading

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands.clear_current_scope import ClearCurrentScopeCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.register_dependency import RegisterDependencyCommand
from src.spacebattle.commands.set_current_scope import SetCurrentScopeCommand
from src.spacebattle.common import constants
from src.spacebattle.exceptions.exeptions import ParentScopeMissingException
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy


class TestInitCommand:
    """Тест проверяет базовую настройку команды init и корректную имплементацию базовых функций"""

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

    def test_init_command_set_root_scope(self, initial_state):
        """П4. Тест проверяет что задаются базовые настройки"""
        InitCommand().execute()
        with soft_assertions():
            assert constants.IOC_SCOPE_CURRENT_SET in InitCommand.root_scope
            assert constants.IOC_SCOPE_CURRENT_CLEAR in InitCommand.root_scope
            assert constants.IOC_SCOPE_CURRENT in InitCommand.root_scope
            assert constants.IOC_SCOPE_PARENT in InitCommand.root_scope
            assert constants.IOC_SCOPE_CREATE_EMPTY in InitCommand.root_scope
            assert constants.IOC_SCOPE_CREATE in InitCommand.root_scope
            assert constants.IOC_REGISTER in InitCommand.root_scope
            assert isinstance(InitCommand.root_scope[constants.IOC_SCOPE_CURRENT_SET](None), SetCurrentScopeCommand)
            assert isinstance(InitCommand.root_scope[constants.IOC_SCOPE_CURRENT_CLEAR](), ClearCurrentScopeCommand)
            assert isinstance(InitCommand.root_scope[constants.IOC_REGISTER](None, None), RegisterDependencyCommand)
            assert InitCommand.already_executed_successfully

    def test_init_command_not_reinitialize_root_scope(self, initial_state):
        """П4. Тест проверяет что не происходит повторной инициализации при повторном вызове команды"""
        InitCommand().execute()
        InitCommand.root_scope = {}
        InitCommand().execute()
        assert InitCommand.root_scope == {}

    def test_init_command_current_scope_default_root(self, initial_state):
        """П4. Тест проверяет что текущий scope по умолчанию root"""
        InitCommand().execute()
        current_scope = IoC.resolve(constants.IOC_SCOPE_CURRENT)
        assert current_scope == InitCommand.root_scope

    def test_init_command_current_set(self, initial_state):
        """П4. Тест проверяет корректную имплементацию команды SET"""
        InitCommand().execute()
        IoC.resolve(constants.IOC_SCOPE_CURRENT_SET, lambda: 1).execute()
        assert InitCommand.current_scope.value() == 1

    def test_init_command_current_clear(self, initial_state):
        """П4. Тест проверяет корректную имплементацию команды CLEAR"""
        InitCommand().execute()
        scope = IoC.resolve(constants.IOC_SCOPE_CREATE)
        IoC.resolve(constants.IOC_SCOPE_CURRENT_SET, scope).execute()
        IoC.resolve(constants.IOC_SCOPE_CURRENT_CLEAR).execute()
        with pytest.raises(AttributeError):
            assert InitCommand.current_scope.value

    def test_init_command_current(self, initial_state):
        """П4. Тест проверяет корректный возврат текущего scope"""
        InitCommand().execute()
        scope = IoC.resolve(constants.IOC_SCOPE_CREATE)
        IoC.resolve(constants.IOC_SCOPE_CURRENT_SET, scope).execute()
        assert scope == IoC.resolve(constants.IOC_SCOPE_CURRENT)

    def test_successful_parent_scope(self, initial_state):
        """П4. Тест проверяет успешный возврат parent scope"""
        InitCommand().execute()
        parent_scope = IoC.resolve(constants.IOC_SCOPE_CREATE)
        child_scope = IoC.resolve(constants.IOC_SCOPE_CREATE, parent_scope)
        IoC.resolve(constants.IOC_SCOPE_CURRENT_SET, child_scope).execute()
        assert IoC.resolve(constants.IOC_SCOPE_PARENT) == parent_scope

    def test_unsuccessful_init_command_parent(self, initial_state):
        """П4. Тест проверяет что отсутствует parent scope по умолчанию"""
        InitCommand().execute()
        with pytest.raises(ParentScopeMissingException):
            assert IoC.resolve(constants.IOC_SCOPE_PARENT)

    def test_init_command_create_empty(self, initial_state):
        """П4. Тест проверяет что создается пустой словарь"""
        InitCommand().execute()
        assert IoC.resolve(constants.IOC_SCOPE_CREATE_EMPTY) == {}

    def test_init_command_register(self, initial_state):
        """П4. Тест проверяет регистрацию новой зависимости"""
        InitCommand().execute()
        IoC.resolve(constants.IOC_REGISTER, "Test.Dependency", lambda: 1).execute()
        assert IoC.resolve("Test.Dependency") == 1

    def test_unsuccessful_init_command_dependency(self, initial_state):
        InitCommand().execute()
        with pytest.raises(ParentScopeMissingException):
            assert IoC.resolve("UNAVAILABLE_DEPENDENCY")
