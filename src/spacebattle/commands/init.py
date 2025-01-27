from src.spacebattle.commands.clear_current_scope import ClearCurrentScopeCommand
from src.spacebattle.commands.command import Command
from src.spacebattle.commands.register_dependency import RegisterDependencyCommand
from src.spacebattle.commands.set_current_scope import SetCurrentScopeCommand
from src.spacebattle.exceptions.exeptions import ParentScopeMissingException
from src.spacebattle.scopes.dependency_resolver import DependencyResolver
from src.spacebattle.scopes.ioc import IoCContainer


def _ioc_scope_parent():
    raise ParentScopeMissingException("Отсутствует родительский scope")


def _ioc_scope_create(scope: dict, *args):
    creating_scope = scope["IoC.Scope.Create.Empty"]()
    if args:
        creating_scope["IoC.Scope.Parent"] = args[0]
    else:
        parent_scope = scope["IoC.Scope.Current"]
        creating_scope["IoC.Scope.Parent"] = lambda: parent_scope
    return creating_scope


class InitCommand(Command):
    def __init__(self):
        self.scope = dict()

    def execute(self):
        self.scope["IoC.Scope.Current.Set"] = lambda scope: SetCurrentScopeCommand(self, scope)
        self.scope["IoC.Scope.Current.Clear"] = lambda: ClearCurrentScopeCommand(self)
        self.scope["IoC.Scope.Current"] = lambda: self.scope
        self.scope["IoC.Scope.Parent"] = lambda: _ioc_scope_parent
        self.scope["IoC.Scope.Create.Empty"] = lambda: {}
        self.scope["IoC.Scope.Create"] = lambda *args: _ioc_scope_create(self.scope, *args)
        self.scope["IoC.Register"] = lambda dependency, strategy: RegisterDependencyCommand(
            dependency=dependency, strategy=strategy
        )
        IoCContainer.resolve(
            "Update.Ioc.Resolve.Dependency.Strategy",
            lambda old_strategy: lambda dependency, *args: DependencyResolver(self.scope).resolve(dependency, *args),
        ).execute()
