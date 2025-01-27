class DependencyResolver:
    def __init__(self, scope: dict):
        self._dependencies = scope

    def resolve(self, dependency, *args):
        dependencies = self._dependencies
        while True:
            if dependency in dependencies:
                dependency_resolver_strategy = dependencies[dependency]
                return dependency_resolver_strategy(*args)
            else:
                parent_scope = dependencies["IoC.Scope.Parent"]
                print(args)
                dependencies = parent_scope(*args)

    """
    def resolve(self, dependency: str, *args):
        return self._scope[dependency](*args)
    """
