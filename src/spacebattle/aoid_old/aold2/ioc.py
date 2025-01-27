from src.spacebattle.commands.command import Command


class UpdateIocResolveDependencyStrategyCommand(Command):
    def __init__(self, updater):
        self._update_ioc_strategy = updater

    def execute(self):
        IoCContainer.strategy = self._update_ioc_strategy(IoCContainer.strategy)


class IoCContainer:
    """
    strategy = lambda dependency, *args: (
        UpdateIocResolveDependencyStrategyCommand(args[0])
        if dependency == "Update.Ioc.Resolve.Dependency.Strategy"
        else KeyError(f"Dependency {dependency} is not found.")
    )

    @staticmethod
    def resolve(dependency, *args):
        return IoCContainer.strategy(dependency, *args)
    """

    """
    @staticmethod
    def resolve(dependency: str, *args):
        if dependency == "Update.Ioc.Resolve.Dependency.Strategy":
            IoCContainer.scope = args[0]()
            #IoCContainer.scope = args[0](IoCContainer.scope)
            #IoCContainer.scope = args[0](IoCContainer.scope)
            #IoCContainer.scope = args[0](dependency, *args)
            #return IoCContainer.scope[dependency](*args)
        else:
            return IoCContainer.scope[dependency](*args)
    """
