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
        parent_scope = args[0]
        creating_scope["IoC.Scope.Parent"] = lambda *args: parent_scope
    else:
        parent_scope = scope["IoC.Scope.Current"]
        creating_scope["IoC.Scope.Parent"] = lambda *args: parent_scope
    return creating_scope


class InitCommand(Command):
    scope = dict()

    def execute(self):
        InitCommand.scope["IoC.Scope.Current.Set"] = lambda *args: SetCurrentScopeCommand(*args)
        InitCommand.scope["IoC.Scope.Current.Clear"] = lambda *args: ClearCurrentScopeCommand()
        InitCommand.scope["IoC.Scope.Current"] = lambda *args: InitCommand.scope
        InitCommand.scope["IoC.Scope.Parent"] = lambda *args: _ioc_scope_parent
        InitCommand.scope["IoC.Scope.Create.Empty"] = lambda *args: {}
        InitCommand.scope["IoC.Scope.Create"] = lambda *args: _ioc_scope_create(InitCommand.scope, *args)
        InitCommand.scope["IoC.Register"] = lambda dependency, strategy: RegisterDependencyCommand(
            dependency=dependency, strategy=strategy
        )
        IoCContainer.resolve(
            "Update.Ioc.Resolve.Dependency.Strategy",
            lambda old_strategy: lambda dependency, *args: DependencyResolver(InitCommand.scope).resolve(
                dependency, *args
            ),
        ).execute()
