from src.spacebattle.aold2.dependency_resolver import DependencyResolver
from src.spacebattle.aold2.ioc import IoCContainer
from src.spacebattle.aold2.register_dependency import RegisterDependencyCommand
from src.spacebattle.commands.command import Command
from src.spacebattle.exceptions.exeptions import ParentScopeMissingException


def ioc_scope_parent():
    raise ParentScopeMissingException("Отсутствует родительский scope")


def resolve_dependency(scope, dependency, *args):
    resolver = DependencyResolver(scope)
    return resolver.resolve(dependency, *args)


def create_scope(*args):
    creating_scope = IoCContainer.resolve("IoC.Scope.Create.Empty")

    if args:
        parent_scope = args[0]
        creating_scope["IoC.Scope.Parent"] = lambda *args: parent_scope
    else:
        parent_scope = IoCContainer.resolve("IoC.Scope.Current")
        creating_scope["IoC.Scope.Parent"] = lambda *args: parent_scope

    return creating_scope


class InitCommand(Command):
    def execute(self):
        scope = dict(
            {
                "IoC.Scope.Parent": lambda args: Exception("The root scope has no a parent scope."),
                "IoC.Scope.Current": lambda: scope,
                "IoC.Scope.Create.Empty": lambda: {},
                "IoC.Scope.Create": lambda: dict({"IoC.Scope.Parent": scope}),
                "IoC.Register": lambda dependency, strategy: RegisterDependencyCommand(
                    dependency=dependency, strategy=strategy
                ),
            }
        )
        # IoCContainer.scope = scope
        # IoCContainer.resolve(
        #    "Update.Ioc.Resolve.Dependency.Strategy",
        #    lambda strategy: lambda dependency, *args: DependencyResolver(scope).resolve(dependency, *args)
        # )
        IoCContainer.resolve(
            "Update.Ioc.Resolve.Dependency.Strategy",
            lambda dependency, *args: resolve_dependency(scope, dependency, *args),
        ).execute()
