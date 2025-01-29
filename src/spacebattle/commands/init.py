from src.spacebattle.commands.clear_current_scope import ClearCurrentScopeCommand
from src.spacebattle.commands.command import Command
from src.spacebattle.commands.register_dependency import RegisterDependencyCommand
from src.spacebattle.commands.set_current_scope import SetCurrentScopeCommand
from src.spacebattle.exceptions.exeptions import ParentScopeMissingException
from src.spacebattle.scopes.dependency_resolver import DependencyResolver
from src.spacebattle.scopes.ioc import IoCContainer


def _ioc_scope_parent():
    raise ParentScopeMissingException("Отсутствует родительский scope")


def _ioc_scope_create(*args):
    creating_scope = IoCContainer.resolve("IoC.Scope.Create.Empty")
    if args:
        creating_scope["IoC.Scope.Parent"] = lambda *a: args[0]
    else:
        creating_scope["IoC.Scope.Parent"] = lambda *a: IoCContainer.resolve("IoC.Scope.Current")
    return creating_scope


class InitCommand(Command):
    root_scope = dict()
    current_scope = dict()

    def execute(self):
        InitCommand.root_scope["IoC.Scope.Current.Set"] = lambda *args: SetCurrentScopeCommand(*args)
        InitCommand.root_scope["IoC.Scope.Current.Clear"] = lambda *args: ClearCurrentScopeCommand()
        InitCommand.root_scope["IoC.Scope.Current"] = (
            lambda *args: InitCommand.current_scope if InitCommand.current_scope else InitCommand.root_scope
        )
        InitCommand.root_scope["IoC.Scope.Parent"] = lambda *args: _ioc_scope_parent()
        InitCommand.root_scope["IoC.Scope.Create.Empty"] = lambda *args: {}
        InitCommand.root_scope["IoC.Scope.Create"] = lambda *args: _ioc_scope_create(*args)
        InitCommand.root_scope["IoC.Register"] = lambda dependency, strategy: RegisterDependencyCommand(
            dependency=dependency, strategy=strategy
        )
        IoCContainer.resolve(
            "Update.Ioc.Resolve.Dependency.Strategy",
            lambda old_strategy: lambda dependency, *args: DependencyResolver(
                InitCommand.current_scope if InitCommand.current_scope else InitCommand.root_scope
            ).resolve(dependency, *args),
        ).execute()
