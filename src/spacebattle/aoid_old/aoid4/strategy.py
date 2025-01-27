def _strategy(dependency, *args):
    from src.spacebattle.aoid4.update_ioc_resolve_dependency_strategy import (
        UpdateIocResolveDependencyStrategyCommand,
    )

    if dependency == "Update.Ioc.Resolve.Dependency.Strategy":
        return UpdateIocResolveDependencyStrategyCommand(args[0])
    else:
        raise KeyError(f"Dependency {dependency} is not found.")
