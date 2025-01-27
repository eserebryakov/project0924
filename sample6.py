from src.spacebattle.aoid4.init import InitCommand

# IoCContainer.resolve("test1", 2, 3)


init_command = InitCommand()
init_command.execute()


# scope1 = IoCContainer.resolve("IoC.Scope.Create")
# IoCContainer.resolve("IoC.Scope.Current.Set", scope1).execute()
# IoCContainer.resolve("IoC.Register", "test", lambda: 5).execute()
# print(IoCContainer.resolve("test"))
# print(IoCContainer.resolve("IoC.Scope.Current"))
# IoCContainer.resolve("IoC.Scope.Current.Set", scope1).execute()
# IoCContainer.resolve("IoC.Register", "test", lambda: 5).execute()
# print(IoCContainer.resolve("IoC.Scope.Cu2rrent"))
# print(scope1)
# print(IoCContainer.resolve("IoC.Scope.Current"))
# print(IoCContainer.resolve("IoC.Scope.Parent"))

# print(IoCContainer.resolve("IoC.Scope.Current"))
# IoCContainer.resolve("IoC.Register", "test", lambda: 3).execute()
# print(IoCContainer.resolve("IoC.Scope.Current"))

# print(IoCContainer.resolve("test"))
# print(IoCContainer.resolve("IoC.Scope.Create")["IoC.Scope.Parent"]()()["IoC.Scope.Parent"]()())
# IoCContainer.resolve("IoC.Scope.Current.Clear").execute()
