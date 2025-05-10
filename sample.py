import threading

from src.spacebattle.commands.init import InitCommand


def task():
    init_command = InitCommand()
    init_command.execute()

    # ClearCurrentScopeCommand()
    print(init_command.root_scope)


threads = []
for i in range(1):
    t = threading.Thread(target=task)
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()
