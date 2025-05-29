import threading
from queue import Queue

from src.spacebattle.common.constants import IOC_HANDLE_EXCEPTION
from src.spacebattle.scopes.ioc import IoC


class ServerThread:
    def __init__(self, queue: Queue):
        self.__stop_event = threading.Event()
        self.__queue = queue
        self.__thread = threading.Thread(target=self.__run_loop)
        self.behaviour = self.__default_behaviour
        self.__lock = threading.Lock()

    def __default_behaviour(self):
        command = self.__queue.get()
        try:
            command.execute()
        except Exception as e:
            IoC.resolve(IOC_HANDLE_EXCEPTION, command, e).execute()

    def __run_loop(self):
        while not self.__stop_event.is_set():
            self.behaviour()

    @property
    def queue(self):
        return self.__queue

    @property
    def is_running(self):
        return self.__thread.is_alive()

    def start(self):
        self.__thread.start()

    def stop(self):
        self.__stop_event.set()

    def set_behaviour(self, behaviour):
        with self.__lock:
            self.behaviour = behaviour
