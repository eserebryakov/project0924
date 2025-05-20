from src.spacebattle.commands.command import Command


class SetAttributeValueCommand(Command):
    """Класс (команда) которая устанавливает значение атрибута"""

    def __init__(self, obj, attribute, value, strategy):
        self.__obj = obj
        self.__attribute = attribute
        self.__value = value
        self.__strategy = strategy

    def execute(self):
        self.__strategy(self.__obj, self.__attribute, self.__value).resolve()
