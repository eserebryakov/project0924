from src.spacebattle.commands.command import Command
from src.spacebattle.commands.handle_exception import HandleExceptionCommand
from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common.constants import (
    IOC_HANDLE_EXCEPTION,
    IOC_REGISTER,
    IOC_THREAD_ID,
)
from src.spacebattle.scopes.ioc import IoC

init_command = InitCommand()
init_command.execute()


class MockException(Exception):
    ...


class MockCommand(Command):
    def execute(self):
        raise MockException("MockException")


IoC.resolve(IOC_REGISTER, IOC_HANDLE_EXCEPTION, lambda c_, e_: HandleExceptionCommand(c_, e_)).execute()


start_command = StartCommand()
start_command.execute()


server_ = IoC.resolve(IOC_THREAD_ID)
server_.queue.put(MockCommand())
server_.queue.put(MockCommand())
server_.queue.put(HardStopCommand(server_))
server_.queue.put(MockCommand())
server_.queue.put(MockCommand())


"""
stop = False

queue_ = queue.Queue()
queue_.put(MockCommand())
queue_.put(MockCommand())


def func1():
    while not stop:
        command = queue_.get()
        try:
            command.execute()
        except Exception as e:
            IoC.resolve(IOC_HANDLE_EXCEPTION, command, e).execute()


from queue import Queue

class ServerThread:

    def __init__(self, queue: Queue):
        self.__stop = False
        self.__queue = queue
        self.__thread = threading.Thread(target=func1)

    def start(self):
        self.__thread.start()



server = ServerThread(queue_)
server.start()


queue_.put(MockCommand())
"""
