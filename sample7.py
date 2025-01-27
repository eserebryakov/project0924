from src.spacebattle.commands.init import InitCommand
from src.spacebattle.scopes.ioc import IoCContainer

init_command = InitCommand()
init_command.execute()
scope1 = IoCContainer.resolve("IoC.Scope.Create")
print(scope1)
# IoCContainer.resolve("IoC.Scope.Current.Set", scope1).execute()
# IoCContainer.resolve("IoC.Register", "test", lambda: 5).execute()
# print(IoCContainer.resolve("IoC.Scope.Current"))

# scope1 = IoCContainer.resolve("IoC.Scope.Create")
# print(scope1)
# IoCContainer.resolve("IoC.Scope.Current.Set", scope1).execute()
# IoCContainer.resolve("IoC.Register", "test", lambda: 5).execute()
# print(scope1)

# print(init_command.scope)
# print(len(init_command.scope))
# IoCContainer.resolve("IoC.Register", "test", lambda: 5).execute()
# print(init_command.scope)
# scope1 = IoCContainer.resolve("IoC.Scope.Create")
# print(scope1)
# IoCContainer.resolve("IoC.Scope.Current.Set", scope1).execute()
# IoCContainer.resolve("IoC.Register", "test", lambda: 1)
# print(init_command.scope)
