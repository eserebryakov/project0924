def _strategy(dependency, *args):
    from src.spacebattle.commands.update_ioc_resolve_dependency_strategy import (  # Импорт здесь, чтобы избежать циклического импорта
        UpdateIocResolveDependencyStrategyCommand,
    )

    if dependency == "Update.Ioc.Resolve.Dependency.Strategy":
        return UpdateIocResolveDependencyStrategyCommand(args[0])
    else:
        raise KeyError(f"Dependency {dependency} is not found.")
