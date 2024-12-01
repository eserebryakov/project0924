from src.spacebattle.angle import Angle
from src.spacebattle.commands.fuel_command import (
    BurnFuelCommand,
    BurningObject,
    CheckFuelCommand,
)
from src.spacebattle.commands.simple_macro_command import SimpleMacroCommand
from src.spacebattle.fuel import Fuel
from src.spacebattle.move import MoveCommand, MovingObject
from src.spacebattle.rotate import RotateCommand, RotatingObject
from src.spacebattle.vector import Vector


class SpaseShip(MovingObject, RotatingObject, BurningObject):
    def __init__(self, vector: Vector, angle: Angle, fuel: Fuel):
        self.vector = vector
        self.angle = angle
        self.fuel = fuel

    def get_location(self) -> Vector:
        return self.vector

    def set_location(self, value: Vector) -> None:
        self.vector = value

    def get_velocity(self) -> Vector:
        return Vector(2, 0)

    def get_angle(self) -> Angle:
        return self.angle

    def set_angle(self, value: Angle) -> None:
        self.angle = value

    def get_angular_velocity(self) -> Angle:
        return Angle(1, 4)

    def get_fuel(self) -> Fuel:
        return self.fuel

    def set_fuel(self, value: Fuel) -> None:
        self.fuel = value

    def get_fuel_velocity(self) -> Fuel:
        return Fuel(2)


space_ship = SpaseShip(vector=Vector(5, 5), angle=Angle(0, 4), fuel=Fuel(5))

move_command = MoveCommand(space_ship)
rotate_command = RotateCommand(space_ship)
check_fuel_command = CheckFuelCommand(space_ship)
burn_fuel_command = BurnFuelCommand(space_ship)

move_strait_line_command = SimpleMacroCommand(commands=[check_fuel_command, move_command, burn_fuel_command])

move_strait_line_command.execute()
print(space_ship.get_fuel())
