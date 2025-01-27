from src.spacebattle.aold.register import RegisterCommand
from src.spacebattle.commands.change_velocity import ChangeVelocityCommand
from src.spacebattle.commands.macro import straight_line_command
from src.spacebattle.commands.move import MoveCommand
from src.spacebattle.common.angle import Angle
from src.spacebattle.common.fuel import Fuel
from src.spacebattle.common.vector import Vector
from src.spacebattle.objects.burning import BurningObject
from src.spacebattle.objects.moving import MovingObject


class MockMovingObject(MovingObject, BurningObject):
    def get_location(self) -> Vector:
        return Vector(1, 1)

    def set_location(self, value: Vector) -> None:
        print(value)

    def get_velocity(self) -> Vector:
        return Vector(1, 1)

    def get_fuel(self) -> Fuel:
        return Fuel(10)

    def set_fuel(self, value: Fuel) -> None:
        print(value)

    def get_fuel_velocity(self) -> Fuel:
        return Fuel(5)


object_ = MockMovingObject()

vector = Vector(1, 2)
angle = Angle(1, 2)
fuel = Fuel(10)


# storage = {
#    "Commands.Move": lambda *args, **kwargs: MoveCommand(*args, **kwargs),
#    "Commands.ChangeVelocity": lambda *args, **kwargs: ChangeVelocityCommand(*args, **kwargs)
# }

storage = {"IoC.Register": lambda *args, **kwargs: RegisterCommand(*args, **kwargs)}


class IoCContainer:
    @staticmethod
    def resolve(key: str, *args, **kwargs):
        return storage[key](*args, **kwargs)


print(storage)
IoCContainer.resolve(
    key="IoC.Register", storage=storage, dependency="Commands.Move", strategy=lambda _: MoveCommand(_)
).execute()
IoCContainer.resolve(
    key="IoC.Register",
    storage=storage,
    dependency="Commands.ChangeVelocity",
    strategy=lambda *args, **kwargs: ChangeVelocityCommand(*args, **kwargs),
).execute()
IoCContainer.resolve(
    key="IoC.Register", storage=storage, dependency="Commands.StraightLine", strategy=lambda _: straight_line_command(_)
).execute()

print(storage)

move_command2 = IoCContainer.resolve("Commands.Move", object_)
print(move_command2)
move_command2.execute()
change_velocity = IoCContainer.resolve("Commands.ChangeVelocity", vector, angle)
print(change_velocity)
print(vector)
change_velocity.execute()
print(vector)


IoCContainer.resolve("Commands.StraightLine", object_).execute()
