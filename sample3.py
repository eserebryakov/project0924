from collections.abc import Callable


class ParentScopeMissingException(Exception):
    ...


class IoCContainer:
    scope = None

    @staticmethod
    def resolve(dependency: str, *args):
        return IoCContainer.scope[dependency](*args)


class RegisterDependencyCommand:
    def __init__(self, dependency: str, strategy: Callable):
        self.dependency = dependency
        self.strategy = strategy

    def execute(self):
        current_scope = IoCContainer.scope["IoC.Scope.Current"]()
        current_scope[self.dependency] = self.strategy


def ioc_scope_parent():
    raise ParentScopeMissingException("Отсутствует родительский scope")


scope = dict(
    {
        "IoC.Scope.Parent": ioc_scope_parent,
        "IoC.Scope.Current": lambda: scope,
        "IoC.Scope.Create.Empty": lambda: {},
        "IoC.Scope.Create": lambda: dict({"IoC.Scope.Parent": scope}),
        "IoC.Register": lambda dependency, strategy: RegisterDependencyCommand(
            dependency=dependency, strategy=strategy
        ),
    }
)

IoCContainer.scope = scope

print(IoCContainer.scope)

IoCContainer.scope["IoC.Register"]("test", lambda: 1).execute()
print(IoCContainer.scope)
# print(IoCContainer.scope['test']())

print(IoCContainer.resolve("test"))
