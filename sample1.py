from src.spacebattle.commands.clear_current_scope import ClearCurrentScopeCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.register_dependency import RegisterDependencyCommand

IOC_TEST_DEPENDENCY = "IoC.Test.Dependency"

clear_command = ClearCurrentScopeCommand()

# del InitCommand.current_scope.value
clear_command.execute()

InitCommand().execute()
register_dependency = RegisterDependencyCommand(dependency=IOC_TEST_DEPENDENCY, strategy=lambda: "TestStrategy")
register_dependency.execute()
