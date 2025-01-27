from abc import ABC, abstractmethod


class IDependencyResolver(ABC):
    @abstractmethod
    def resolve(self, dependency: str, *args):
        ...


class DependencyResolver(IDependencyResolver):
    def __init__(self, scope: dict):
        self._scope = scope

    def resolve(self, dependency: str, *args):
        return self._scope[dependency](*args)
