from queue import Queue

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.handle_exception import HandleExceptionCommand
from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.soft_stop import SoftStopCommand
from src.spacebattle.common.constants import IOC_HANDLE_EXCEPTION, IOC_REGISTER
from src.spacebattle.core.server import ServerThread
from src.spacebattle.scopes.ioc import IoC

init_command = InitCommand()
init_command.execute()


class MockException(Exception):
    ...


class MockCommand(Command):
    def execute(self):
        raise MockException("MockException")


IoC.resolve(IOC_REGISTER, IOC_HANDLE_EXCEPTION, lambda c_, e_: HandleExceptionCommand(c_, e_)).execute()

queue_ = Queue()
server = ServerThread(queue_)


queue_.put(MockCommand())
queue_.put(MockCommand())
# queue_.put(HardStopCommand(server))
queue_.put(SoftStopCommand(server))
queue_.put(MockCommand())
queue_.put(MockCommand())


server.start()
# server.stop()
