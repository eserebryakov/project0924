import threading

from src.spacebattle.aoid4.clear_current_scope import ClearCurrentScopeCommand
from src.spacebattle.aoid4.dependency_resolver import DependencyResolver
from src.spacebattle.aoid4.ioc import IoCContainer
from src.spacebattle.aoid4.register_dependency import RegisterDependencyCommand
from src.spacebattle.aoid4.set_current_scope import SetCurrentScopeCommand

from src.spacebattle.commands.command import Command


class InitCommand(Command):
    current_scopes = threading.local()
    root_scope = dict()
    already_executed_successfully = False

    def execute(self):
        if InitCommand.already_executed_successfully:
            return

        with threading.Lock():
            if "IoC.Scope.Current.Set" not in InitCommand.root_scope:
                InitCommand.root_scope["IoC.Scope.Current.Set"] = lambda args: SetCurrentScopeCommand(args[0])

            if "IoC.Scope.Current.Clear" not in InitCommand.root_scope:
                InitCommand.root_scope["IoC.Scope.Current.Clear"] = lambda args: ClearCurrentScopeCommand()

            if "IoC.Scope.Current" not in InitCommand.root_scope:
                InitCommand.root_scope["IoC.Scope.Current"] = (
                    lambda args: InitCommand.current_scopes.value
                    if hasattr(InitCommand.current_scopes, "value")
                    else InitCommand.root_scope
                )

            if "IoC.Scope.Parent" not in InitCommand.root_scope:
                InitCommand.root_scope["IoC.Scope.Parent"] = lambda args: Exception(
                    "The root scope has no a parent scope."
                )

            if "IoC.Scope.Create.Empty" not in InitCommand.root_scope:
                InitCommand.root_scope["IoC.Scope.Create.Empty"] = lambda args: {}

            if "IoC.Scope.Create" not in InitCommand.root_scope:
                InitCommand.root_scope["IoC.Scope.Create"] = lambda args: self.create_scope(args)

            if "IoC.Register" not in InitCommand.root_scope:
                InitCommand.root_scope["IoC.Register"] = lambda args: RegisterDependencyCommand(args[0], args[1])

            # print(InitCommand.root_scope)
            IoCContainer.resolve(
                "Update.Ioc.Resolve.Dependency.Strategy",
                lambda old_strategy: lambda dependency, args: DependencyResolver(
                    InitCommand.current_scopes.value
                    if hasattr(InitCommand.current_scopes, "value")
                    else InitCommand.root_scope
                ).resolve(dependency, *args),
            ).execute()
            InitCommand.already_executed_successfully = True

    def create_scope(self, args):
        creating_scope = IoCContainer.resolve("IoC.Scope.Create.Empty")

        if args:
            parent_scope = args[0]
            creating_scope["IoC.Scope.Parent"] = lambda args: parent_scope
        else:
            parent_scope = IoCContainer.resolve("IoC.Scope.Current")
            creating_scope["IoC.Scope.Parent"] = lambda args: parent_scope

        return creating_scope
