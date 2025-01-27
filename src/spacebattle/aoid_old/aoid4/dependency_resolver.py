from abc import ABC, abstractmethod


class IDependencyResolver(ABC):
    @abstractmethod
    def resolve(self, dependency: str, args):
        ...


class DependencyResolver(IDependencyResolver):
    def __init__(self, scope: dict):
        self._dependencies = scope
        print(self._dependencies)

    def resolve(self, dependency, args):
        dependencies = self._dependencies

        while True:
            if dependency in dependencies:
                dependency_resolver_strategy = dependencies[dependency]
                return dependency_resolver_strategy(args)
            else:
                parent_scope = dependencies["IoC.Scope.Parent"]
                dependencies = parent_scope(args)
