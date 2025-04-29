from src.spacebattle.common import constants


class DependencyResolver:
    def __init__(self, scope: dict):
        self._dependencies = scope
        # print(self._dependencies)

    def resolve(self, dependency, *args):
        dependencies = self._dependencies
        while True:
            if dependency in dependencies:
                dependency_resolver_strategy = dependencies[dependency]
                return dependency_resolver_strategy(*args)
            else:
                parent_scope = dependencies[constants.IOC_SCOPE_PARENT]
                dependencies = parent_scope(*args)
