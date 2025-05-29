from queue import Queue

from src.spacebattle.common.constants import IOC_QUEUE, IOC_REGISTER
from src.spacebattle.scopes.ioc import IoC

queue = Queue()
IoC.resolve(IOC_REGISTER, IOC_QUEUE, lambda *args: queue)
