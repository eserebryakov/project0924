import time
from queue import Queue
from uuid import uuid4

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.hard_stop_macro import HardStopMacroCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.move_to import MoveToCommand
from src.spacebattle.commands.run import RunCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common import constants
from src.spacebattle.core.state import Context
from src.spacebattle.scopes.ioc import IoC


class MockCommand(Command):
    def execute(self):
        print("mock command execute")


class MockCommand2(Command):
    def execute(self):
        print("mock command 2 execute")


InitCommand().execute()
game_id = uuid4()

start_command = StartCommand(game_id)
start_command.execute()

IoC.resolve(constants.IOC_REGISTER, "NEW_QUEUE", lambda: Queue()).execute()
new_queue = IoC.resolve("NEW_QUEUE")

server = IoC.resolve(f"{constants.IOC_THREAD}.{game_id}")
queue_one = IoC.resolve(f"{constants.IOC_QUEUE}.{game_id}")

hard_stop = HardStopCommand(server)

context = Context()

move_to_command = MoveToCommand(server, context, new_queue)
run_command = RunCommand(server, context)
hard_stop_macro = HardStopMacroCommand(server, context)


queue_one.put(MockCommand())
queue_one.put(move_to_command)
queue_one.put(move_to_command)
queue_one.put(run_command)
queue_one.put(move_to_command)
queue_one.put(MockCommand())
queue_one.put(hard_stop)


time.sleep(0.1)
print(new_queue.qsize())


"""
InitCommand().execute()
game_id = uuid4()

start_command = StartCommand(game_id)
start_command.execute()

IoC.resolve(constants.IOC_REGISTER, "NEW_QUEUE", lambda: Queue()).execute()
new_queue = IoC.resolve("NEW_QUEUE")

server = IoC.resolve(f"{constants.IOC_THREAD}.{game_id}")
queue_one = IoC.resolve(f"{constants.IOC_QUEUE}.{game_id}")

hard_stop = HardStopCommand(server)
move_to_command = MoveToCommand()

context = Context(server)
context.handle()

queue_one.put(MockCommand())
queue_one.put(MockCommand())
queue_one.put(hard_stop)
"""

"""
queue_one.put(MockCommand())
time.sleep(0.1)
context.handle()
time.sleep(0.1)
queue_one.put(MockCommand())
time.sleep(0.1)
#queue_one.put(move_to_command)
time.sleep(0.1)
queue_one.put(MockCommand2())

time.sleep(0.1)

print(f"q1 {queue_one.qsize()}")
print(f"q2 {new_queue.qsize()}")
"""


"""
InitCommand().execute()
game_id = uuid4()

start_command = StartCommand(game_id)
start_command.execute()


server = IoC.resolve(f"{constants.IOC_THREAD}.{game_id}")
queue_one = IoC.resolve(f"{constants.IOC_QUEUE}.{game_id}")

IoC.resolve(constants.IOC_REGISTER, "QUEUE_TWO", lambda: Queue()).execute()
queue_two = IoC.resolve("QUEUE_TWO")
print(InitCommand.root_scope)

class MockCommand(Command):
    def execute(self):
        print("mock command execute")

hard_stop = HardStopCommand(server)

class CommandProcessor:

    def __init__(self, server_):
        self.state = NormalState()
        self.server = server_
        self.behaviour = server.behaviour

    def handle(self):
        self.state.handle()


command_processor = CommandProcessor(server)
command_processor.handle()

queue_one.put(MockCommand())
queue_one.put(hard_stop)
time.sleep(0.1)
print(server.is_running)
"""


"""
class MockCommand(Command):
    def execute(self):
        print("mock command execute")


queue = Queue()
server = ServerThread(queue)
hard_stop = HardStopCommand(server)

server.start()
print(server.is_running)
queue.put(MockCommand())
queue.put(hard_stop)
time.sleep(0.1)
print(server.is_running)


class CommandProcessor:

    def __init__(self):
        self.state = NormalState()
"""
