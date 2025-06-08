import importlib.util

from src.spacebattle.common.vector import Vector


def _load_plugin(plugin_path: str):
    spec = importlib.util.spec_from_file_location("plugin", plugin_path)
    plugin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin)
    return plugin


teleport_command_plugin = _load_plugin("src/spacebattle/commands/teleport.py")
TeleportCommand = teleport_command_plugin.TeleportCommand

teleportable_object_plugin = _load_plugin("src/spacebattle/objects/teleportable.py")
TeleportableObject = teleportable_object_plugin.TeleportableObject


class ValidObject(TeleportableObject):
    def __init__(self):
        self.location = Vector(0, 0)

    def set_teleport_location(self, value: Vector):
        self.location = value


class TestTeleport:
    def test_teleport(self):
        """Тест проверяет работу команды мгновенной телепортации через динамический плагин"""
        obj = ValidObject()
        teleport_command = TeleportCommand(obj, Vector(10, 10))
        teleport_command.execute()
        assert obj.location == Vector(10, 10)
