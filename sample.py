from src.spacebattle.commands.init import InitCommand
from src.spacebattle.scopes.ioc import IoCContainer

init_command = InitCommand()
init_command.execute()

print(init_command.root_scope)
IoCContainer.resolve("IoC.Scope.Current.Clear").execute()
print(init_command.root_scope)
# print(IoCContainer.resolve("IoC.Scope.Current"))
