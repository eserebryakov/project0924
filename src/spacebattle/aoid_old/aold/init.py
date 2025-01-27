import logging

from src.spacebattle.commands.command import Command


class InitCommand(Command):
    def __init__(self):
        self.current_scope = {}
        self._root_scope = {}
        self.log = logging.getLogger(__name__)

    def execute(self):
        # self._root_scope["IoC.Scope.Current.Set"] = lambda *args, **kwargs: SetCurrentScopeCommand(*args, **kwargs)
        ...
