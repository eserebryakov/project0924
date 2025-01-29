from src.spacebattle.commands.init import InitCommand
from src.spacebattle.scopes.ioc import IoCContainer

init_command = InitCommand()
init_command.execute()
scope = IoCContainer.resolve("IoC.Scope.Create")
IoCContainer.resolve("IoC.Scope.Current.Set", scope)
print(IoCContainer.resolve("IoC.Scope.Current"))

"""
init_command = InitCommand()
init_command.execute()


IoCContainer.resolve("IoC.Register", "test_root", lambda: "root").execute()

new_scope_0 = IoCContainer.resolve("IoC.Scope.Create")
IoCContainer.resolve("IoC.Scope.Current.Set", new_scope_0).execute()
IoCContainer.resolve("IoC.Register", "test_0", lambda: 0).execute()

new_scope_1 = IoCContainer.resolve("IoC.Scope.Create", new_scope_0)
IoCContainer.resolve("IoC.Scope.Current.Set", new_scope_1).execute()
IoCContainer.resolve("IoC.Register", "test_1", lambda: 1).execute()


new_scope_2 = IoCContainer.resolve("IoC.Scope.Create", new_scope_1)
IoCContainer.resolve("IoC.Scope.Current.Set", new_scope_2).execute()
IoCContainer.resolve("IoC.Register", "test_2", lambda: 2).execute()


print(IoCContainer.resolve("test_2"))
print(IoCContainer.resolve("test_1"))
print(IoCContainer.resolve("test_0"))
print(IoCContainer.resolve("test_root"))
print(IoCContainer.resolve("test_root_3"))
"""
