from src.spacebattle.aold2.register_dependency import RegisterDependencyCommand
from src.spacebattle.aold2.scope import Scope

Scope.scope["IoC.Scope.Current"] = Scope.scope
Scope.scope["IoC.Register"] = lambda dependency, strategy: RegisterDependencyCommand(
    dependency=dependency, strategy=strategy
)


class IoCContainer:
    @staticmethod
    def resolve(dependency: str, *args):
        return Scope.scope[dependency](*args)
