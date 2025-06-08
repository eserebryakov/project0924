from src.spacebattle.common.vector import Vector


def with_velocity_check(check_command_cls, max_velocity: Vector):
    def decorator(command_cls):
        class WrappedCommand(command_cls):
            def __init__(self, obj, *args, **kwargs):
                super().__init__(obj, *args, **kwargs)
                self._velocity_checker = check_command_cls(obj, max_velocity)

            def execute(self):
                self._velocity_checker.execute()
                return super().execute()

        return WrappedCommand

    return decorator
