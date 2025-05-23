import queue

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.handle_exception import HandleExceptionCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.common.constants import IOC_HANDLE_EXCEPTION, IOC_REGISTER
from src.spacebattle.scopes.ioc import IoC

InitCommand().execute()


class MockException(Exception):
    ...


class MockCommand(Command):
    def execute(self):
        raise MockException("MockException")


IoC.resolve(IOC_REGISTER, IOC_HANDLE_EXCEPTION, lambda c_, e_: HandleExceptionCommand(c_, e_)).execute()


stop = False

queue_ = queue.Queue()
queue_.put(MockCommand())

while not stop:
    command = queue_.get()
    try:
        command.execute()
    except Exception as e:
        IoC.resolve(IOC_HANDLE_EXCEPTION, command, e).execute()
