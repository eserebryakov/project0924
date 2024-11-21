from abc import ABC, abstractmethod


class Command(ABC):
    """Абстрактный класс (интерфейс) для команды"""

    @abstractmethod
    def execute(self):
        ...
