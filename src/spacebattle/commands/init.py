from src.spacebattle.commands.command import Command
from src.spacebattle.commands.register_dependency import RegisterDependencyCommand
from src.spacebattle.scopes.dependency_resolver import DependencyResolver
from src.spacebattle.scopes.ioc import IoCContainer


class InitCommand(Command):
    def execute(self):
        scope = dict(
            {
                "IoC.Scope.Current": lambda: scope,
                "IoC.Register": lambda dependency, strategy: RegisterDependencyCommand(
                    dependency=dependency, strategy=strategy
                ),
            }
        )
        IoCContainer.resolve(
            "Update.Ioc.Resolve.Dependency.Strategy",
            lambda old_strategy: lambda dependency, *args: DependencyResolver(scope).resolve(dependency, *args),
        ).execute()
