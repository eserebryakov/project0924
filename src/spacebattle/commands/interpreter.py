from src.spacebattle.commands.command import Command
from src.spacebattle.common import constants
from src.spacebattle.core.commands_mapping import ACTIONS
from src.spacebattle.exceptions import CommandException
from src.spacebattle.scopes.ioc import IoC


class InterpreterCommand(Command):
    def __init__(self, order: dict):
        self.order = order

    def execute(self):
        action = self.order.get(constants.ACTION)
        if action not in ACTIONS:
            raise CommandException(f"Invalid action: {action}")
        object_id, game_id = self.order.get(constants.OBJECT_ID), self.order.get(constants.GAME_ID)
        if object_id and game_id:
            print(object_id)
            object_ = IoC.resolve(constants.GAME_OBJECT, game_id, object_id)
            params = [
                value
                for key, value in self.order.items()
                if key not in (constants.OBJECT_ID, constants.ACTION, constants.GAME_ID)
            ]
            print(object_)
            command = IoC.resolve(ACTIONS[action], object_, *params)
            print(command)
        else:
            print(1)
        """
        object_id = self.order.get(constants.OBJECT_ID)
        if object_id:
            params = [value for key, value in self.order.items() if key not in (constants.OBJECT_ID,constants.ACTION)]
            print(params)
            object_ = IoC.resolve(constants.GAME_OBJECT, )
            #command = IoC.resolve(ACTIONS[action], object_id, params)
            print(object_)
            #command.execute()
        else:
            params = [value for key, value in self.order.items() if key not in (constants.ACTION,)]
        #print(*params)
        """
