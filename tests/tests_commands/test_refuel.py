from src.spacebattle.commands.refuel import RefuelCommand
from src.spacebattle.common import Fuel
from src.spacebattle.objects import BurningObject, FuelingObject


class ValidBurningObject(BurningObject):
    def get_fuel(self) -> Fuel:
        return Fuel(0)

    def set_fuel(self, value: Fuel) -> None:
        assert value == Fuel(7)

    def get_fuel_velocity(self) -> Fuel:
        ...


class ValidFuelingObject(FuelingObject):
    def get_available_fuel(self) -> Fuel:
        return Fuel(20)

    def set_available_fuel(self, value: Fuel) -> None:
        assert value == Fuel(13)


class TestRefuel:
    """Тест проверяющий команду заправляющую топливо"""

    def test_refuel(self):
        """
        П5 Тест проверяет, что для объекта, с кол-вом топлива 10 и сжигающего топливо со скоростью 3
        кол-во топлива меняется на 7
        """
        burning_object = ValidBurningObject()
        fueling_object = ValidFuelingObject()
        moc = RefuelCommand(fueling_object=fueling_object, burning_object=burning_object, fuel_amount=Fuel(7))
        moc.execute()
