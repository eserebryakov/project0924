from src.spacebattle.commands.init import InitCommand

# IoCContainer.resolve("test1", 2, 3)


init_command = InitCommand()
init_command.execute()


# print(IoCContainer.resolve("IoC.Scope.Current"))
# IoCContainer.resolve("IoC.Register", "test", lambda: 3).execute()
# print(IoCContainer.resolve("IoC.Scope.Current"))

# print(IoCContainer.resolve("test"))
# print(IoCContainer.resolve("IoC.Scope.Create")["IoC.Scope.Parent"]()()["IoC.Scope.Parent"]()())
# IoCContainer.resolve("IoC.Scope.Current.Clear").execute()
