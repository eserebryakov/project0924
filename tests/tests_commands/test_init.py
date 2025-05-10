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
    """Тест проверяет базову настройку команды init и корректную имплементацию базовых функций"""

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

    """
    def test_current_scope_should_return_root_scope_by_default(self):
        InitCommand().execute()

        current_scope = IoC.resolve(constants.IOC_SCOPE_CURRENT)
        assert current_scope == InitCommand.root_scope

    def test_current_scope_should_return_thread_local_value_if_set(self):
        InitCommand().execute()

        test_scope = {"test": "value"}
        InitCommand.current_scope.value = test_scope

        current_scope = IoC.resolve(constants.IOC_SCOPE_CURRENT)
        assert current_scope == test_scope

    def test_scope_parent_should_raise_exception(self):
        InitCommand().execute()

        with pytest.raises(ParentScopeMissingException):
            IoC.resolve(constants.IOC_SCOPE_PARENT)

    def test_scope_create_should_create_new_scope_with_parent(self):
        InitCommand().execute()

        parent_scope = InitCommand.root_scope
        new_scope = IoC.resolve(constants.IOC_SCOPE_CREATE, parent_scope)

        assert isinstance(new_scope, dict)
        assert IoC.resolve(constants.IOC_SCOPE_PARENT, new_scope) == parent_scope

    def test_scope_create_should_use_current_scope_as_parent_if_not_provided(self):
        InitCommand().execute()

        new_scope = IoC.resolve(constants.IOC_SCOPE_CREATE)
        assert IoC.resolve(constants.IOC_SCOPE_PARENT, new_scope) == InitCommand.root_scope

    def test_register_dependency_command_should_be_available(self):
        InitCommand().execute()

        command = IoC.resolve(constants.IOC_REGISTER, "test", lambda: "value")
        assert isinstance(command, RegisterDependencyCommand)

    def test_resolve_dependency_strategy_should_be_updated(self):
        InitCommand().execute()

        # Проверяем, что стратегия разрешения зависимостей работает
        test_key = "test.key"
        test_value = "test.value"

        # Регистрируем тестовую зависимость
        IoC.resolve(constants.IOC_REGISTER, test_key, lambda *args: test_value).execute()

        # Проверяем, что можем разрешить зависимость
        resolved = IoC.resolve(test_key)
        assert resolved == test_value

    def test_thread_safety_of_init_command(self):
        InitCommand().execute()

        def thread_func():
            # Проверяем, что в другом потоке current_scope не установлен
            assert not hasattr(InitCommand.current_scope, 'value')
            return IoC.resolve(constants.IOC_SCOPE_CURRENT)

        # Запускаем поток
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(thread_func)
            result = future.result()

        # Проверяем, что в другом потоке возвращается root_scope
        assert result == InitCommand.root_scope
    """
