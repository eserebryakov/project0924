from abc import ABC, abstractmethod


class IDependencyResolver(ABC):
    @abstractmethod
    def resolve(self, dependency: str, *args):
        ...


class DependencyResolver(IDependencyResolver):
    def __init__(self, scope: dict):
        self._scope = scope

    """
    def resolve(self, dependency, *args):
        dependencies = self._dependencies
        #print("========")
        #print(dependencies)
        print(dependency)
        print(dependencies)
        print(len(dependencies))

        while True:
            if dependency in dependencies:
                dependency_resolver_strategy = dependencies[dependency]
                return dependency_resolver_strategy(*args)
            else:
                parent_scope = dependencies['IoC.Scope.Parent']
                print(parent_scope)
                print(*args)
                dependencies = parent_scope(*args)
    """

    def resolve(self, dependency: str, *args):
        return self._scope[dependency](*args)
