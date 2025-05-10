import pytest
from assertpy import soft_assertions

from src.spacebattle.common.constants import IOC_SCOPE_PARENT
from src.spacebattle.exceptions.exeptions import ParentScopeMissingException
from src.spacebattle.scopes.dependency_resolver import DependencyResolver


def _ioc_scope_parent():
    raise ParentScopeMissingException()


TEST_SCOPE_CHILD_1 = "TEST_SCOPE_CHILD_1"
TEST_SCOPE_CHILD_2 = "TEST_SCOPE_CHILD_2"
CHILD_1 = "child_1"
CHILD_2 = "child_2"


class TestDependencyResolver:
    """Тест проверяющий работу функции разрешения зависимостей (дерева зависимостей)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.scope = {
            TEST_SCOPE_CHILD_2: lambda *args: CHILD_2,
            IOC_SCOPE_PARENT: lambda *args: {
                TEST_SCOPE_CHILD_1: lambda *args1: CHILD_1,
                IOC_SCOPE_PARENT: lambda *args2: _ioc_scope_parent(),
            },
        }
        self.dependency_resolver = DependencyResolver(self.scope)

    def test_successful_dependency_resolver_child_2(self):
        """П4. Тест проверяет что resolver успешно возвращает из дерева child 2 (потомка child 1)"""
        assert self.dependency_resolver.resolve(TEST_SCOPE_CHILD_2) == CHILD_2

    def test_successful_dependency_resolver_child_1(self):
        """П4. Тест проверяет что resolver успешно возвращает из дерева child 1 (родителя child 2)"""
        assert self.dependency_resolver.resolve(TEST_SCOPE_CHILD_1) == CHILD_1

    def test_successful_dependency_resolver_parent(self):
        """П4. Тест проверяет что resolver успешно возвращает родительский scope"""
        scope = self.dependency_resolver.resolve(IOC_SCOPE_PARENT)
        with soft_assertions():
            assert IOC_SCOPE_PARENT in scope
            assert TEST_SCOPE_CHILD_1 in scope

    def test_unsuccessful_dependency_resolver_parent(self):
        """П4. Тест (негативный) проверяет что resolver успешно возвращает исключение, если не найден scope"""
        with pytest.raises(ParentScopeMissingException):
            assert self.dependency_resolver.resolve("UNAVAILABLE_SCOPE")
