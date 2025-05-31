from src.spacebattle.commands.command import Command
from src.spacebattle.common import constants
from src.spacebattle.scopes.ioc import IoC


class CreateObjectCommand(Command):
    def __init__(self, game_id: str, object_id: str, obj: dict):
        self.__game_id = game_id
        self.__object_id = object_id
        self.__object = obj

    def execute(self):
        IoC.resolve(
            constants.IOC_REGISTER,
            constants.GAME_OBJECT,
            lambda game_id=self.__game_id, id_=self.__object_id: self.__object,
        ).execute()
