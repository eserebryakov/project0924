import inspect

from src.spacebattle.common import constants
from src.spacebattle.scopes.ioc import IoC


def auto_generate_adapter(class_, obj):
    """Функция автоматически генерирует адаптер."""

    class MetaAdapter(type):
        def __new__(cls, name, bases, attrs):
            for member_ in inspect.getmembers(class_, predicate=inspect.isfunction):
                member = member_[0]
                if member.startswith(constants.PREFIX_GET):
                    key = member.removeprefix(constants.PREFIX_GET)
                    attrs[member] = lambda self, key_=key: IoC.resolve(f"{class_.__name__}.{key_}.get", self)
                elif member.startswith(constants.PREFIX_SET):
                    key = member.removeprefix(constants.PREFIX_SET)
                    attrs[member] = lambda self, value, key_=key: IoC.resolve(
                        f"{class_.__name__}.{key_}.set", self, key_, value
                    ).execute()
                else:
                    attrs[member] = lambda self: setattr(self, member, member_)
                attrs["__init__"] = lambda self, value: setattr(self, "obj", value)
            return type.__new__(cls, name, bases, attrs)

    class Adapter(metaclass=MetaAdapter):
        ...

    return Adapter(obj)
