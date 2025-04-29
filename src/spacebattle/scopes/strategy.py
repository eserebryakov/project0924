from src.spacebattle.common import constants


def _strategy(dependency, *args):
    from src.spacebattle.commands.update_ioc_resolve_dependency_strategy import (
        UpdateIocResolveDependencyStrategyCommand,
    )

    if dependency == constants.UPDATE_IOC_RESOLVE_DEPENDENCY_STRATEGY:
        return UpdateIocResolveDependencyStrategyCommand(args[0])
    else:
        raise KeyError(f"Dependency {dependency} is not found.")
