from src.spacebattle.commands.command import Command


class InterpretCommand(Command):
    def __init__(self, game_id, object_id, operation_id, args):
        self.game_id = game_id
        self.object_id = object_id
        self.operation_id = operation_id
        self.args = args

    def execute(self):
        print(self.game_id, self.object_id, self.operation_id, self.args)
