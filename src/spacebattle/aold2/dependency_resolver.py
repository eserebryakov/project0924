from abc import ABC, abstractmethod


class IDependencyResolver(ABC):
    @abstractmethod
    def resolve(self, dependency: str, *args):
        ...


class DependencyResolver(IDependencyResolver):
    def __init__(self, scope):
        self._dependencies = scope

    def resolve(self, dependency, *args):
        dependencies = self._dependencies

        while True:
            dependency_resolver_strategy = dependencies.get(dependency)
            if dependency_resolver_strategy:
                return dependency_resolver_strategy(*args)
            elif "IoC.Scope.Parent" in dependencies:
                dependencies = dependencies["IoC.Scope.Parent"](*args)
            else:
                raise KeyError(f"{dependency} dependency not found.")


"""
class DependencyResolver(IDependencyResolver):

    def __init__(self, scope: dict):
        self._scope = scope

    def resolve(self, dependency: str, *args):
        return self._scope[dependency](*args)
"""
