import threading
import time

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.scopes.ioc import IoCContainer


def func1():
    init_command = InitCommand()
    init_command.execute()
    # IoCContainer.resolve("IoC.Register", "test", lambda: 1).execute()
    scope = IoCContainer.resolve("IoC.Scope.Create")
    print(scope)
    IoCContainer.resolve("IoC.Scope.Current.Set", scope).execute()
    print(IoCContainer.resolve("IoC.Scope.Current"))


threads = []
for index in range(2):
    time.sleep(1)
    thread = threading.Thread(target=func1)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
