from src.spacebattle.scopes.strategy import _strategy


class IoC:
    strategy = _strategy

    @staticmethod
    def resolve(dependency: str, *args):
        return IoC.strategy(dependency, *args)
