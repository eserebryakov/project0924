from queue import Queue

import pytest
from assertpy import soft_assertions

<<<<<<< HEAD
<<<<<<< HEAD
from src.spacebattle.commands.command import Command
from src.spacebattle.commands.macro import MacroCommand
from src.spacebattle.commands.put import PutCommand
=======
from src.spacebattle.commands import Command, MacroCommand, PutCommand
>>>>>>> d8de736 (DZ3: Добавил домашнее задание по теме Команда)
=======
from src.spacebattle.commands.command import Command
from src.spacebattle.commands.macro import MacroCommand
from src.spacebattle.commands.put import PutCommand
>>>>>>> ed1a774 (DZ4: Добавил домашнее задание по теме Команда)
from src.spacebattle.exceptions import CommandException


class ValidMockCommand0(Command):
    def execute(self):
        ...


class ValidMockCommand1(Command):
    def execute(self):
        ...


_LIST_MOCK_COMMANDS = [ValidMockCommand0(), ValidMockCommand1()]


class ExceptionMockCommand(Command):
    def execute(self):
        raise CommandException("CommandException")


_LIST_EXCEPTION_MOCK_COMMANDS = [ExceptionMockCommand(), ValidMockCommand0()]


class TestMacroCommand:
    """Тест проверяет работу макрокоманды"""

    def test_macro_command(self):
        """П7 Тест проверяет работу макрокоманды (все команды выполняются):
        1. Передаем макрокоманде список команд, каждая их которых кладет в очередь mock команду
        2. Проверяем что в очереди (берем из очереди) находятся mock команды в определенном порядке
        3. Проверяем что после этого очередь пуста
        """
        queue = Queue()
        macro_command = MacroCommand(
            [PutCommand(_LIST_MOCK_COMMANDS[0], queue), PutCommand(_LIST_MOCK_COMMANDS[1], queue)]
        )
        macro_command.execute()
        with soft_assertions():
            assert queue.get() == _LIST_MOCK_COMMANDS[0]
            assert queue.get() == _LIST_MOCK_COMMANDS[1]
            assert queue.qsize() == 0

    def test_raise_exception_macro_command(self):
        """П7 Тест проверяет работу макрокоманды (команда выбрасывает исключение):
        1. Передаем макрокоманде список команд:
            - первая команда с исключением
            - вторая команда кладет в очередь mock команду
        2. Проверяем, что макрокоманда при выполнении первой команды выбросила исключение от этой команды
        3. Проверяем, что команда, которая кладет в очередь mock команду не выполнялась (очередь пуста)
        """
        queue = Queue()
        macro_command = MacroCommand(
            [_LIST_EXCEPTION_MOCK_COMMANDS[0], PutCommand(_LIST_EXCEPTION_MOCK_COMMANDS[1], queue)]
        )
        with pytest.raises(CommandException):
            macro_command.execute()
        with soft_assertions():
            assert queue.qsize() == 0
