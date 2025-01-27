from src.spacebattle.aoid3.strategy import _strategy


class IoCContainer:
    strategy = _strategy

    @staticmethod
    def resolve(dependency: str, *args):
        return IoCContainer.strategy(dependency, *args)
