from src.spacebattle.aold2.init import InitCommand

init_command = InitCommand()
init_command.execute()

# print(IoCContainer)

"""
IoCContainer.resolve("IoC.Register", "test", lambda: 1).execute()
print(IoCContainer.scope)

print(IoCContainer.resolve('test'))


resolver = DependencyResolver(IoCContainer.scope)
print(resolver.resolve('test'))

print(DependencyResolver(IoCContainer.scope).resolve('test'))
"""
