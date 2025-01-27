from src.spacebattle.commands.init import InitCommand
from src.spacebattle.scopes.ioc import IoCContainer

# IoCContainer.resolve("test1", 2, 3)


init_command = InitCommand()
init_command.execute()


print(IoCContainer.resolve("IoC.Scope.Current"))
IoCContainer.resolve("IoC.Register", "test", lambda: 3).execute()
print(IoCContainer.resolve("IoC.Scope.Current"))

print(IoCContainer.resolve("test"))
