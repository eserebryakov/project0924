from uuid import uuid4

from requests import Session

from src.spacebattle.common import constants
from src.spacebattle.common.vector import Vector
from src.spacebattle.core.message import Message

OBJECTS = [
    {
        "object_id": str(uuid4()),
        "location": Vector(2, 2).model_dump(),
        "velocity": Vector(0, 0).model_dump(),
    }
]

session = Session()
response = session.post(url="http://127.0.0.1:5000/api/games/start")
game_id = response.json()["game_id"]
object_id = OBJECTS[0]["object_id"]

response = session.post(
    url=f"http://127.0.0.1:5000/api/games/{game_id}/object",
    json=OBJECTS[0],
)

message = Message(
    game_id=game_id,
    object_id=object_id,
    operation_id=constants.OPERATION_MOVING_STRAIGHT_LINE,
    args=Vector(150, 250),
)


response = session.post(
    url="http://127.0.0.1:5000/api/games/messages",
    json=message.model_dump_json(),
)

print(OBJECTS[0])

"""
message = Message(
    game_id=game_id,
    object_id=game_id,
    operation_id=constants.OPERATION_CREATE_OBJECT,
    args=OBJECTS[0],
)

response = session.post(
    url="http://127.0.0.1:5000/api/games/messages",
    json=message.model_dump_json(),
)
print(response.status_code)
print(response.json())
"""


"""
IoC.resolve(
    constants.IOC_REGISTER,
    f"{constants.GAME_OBJECT}.{OBJECTS[0]['object_id']}",
    lambda : OBJECTS[0]
).execute()

IoC.resolve(
    constants.IOC_REGISTER,
    constants.GAME_OBJECT,
    lambda id_: IoC.resolve(f"{constants.GAME_OBJECT}.{id_}")
).execute()
IoC.resolve(
    constants.IOC_REGISTER,
    constants.ADAPTER,
    lambda class_, obj: auto_generate_adapter(class_, obj)
).execute()

adapter = IoC.resolve(constants.ADAPTER, MovingObject, OBJECTS[0])
IoC.resolve(
    constants.IOC_REGISTER,
    f"{MovingObject.__name__}.location.get",
    lambda obj: DefaultGetPropertyStrategy(obj=obj.obj, attribute="value").resolve(),
).execute()
IoC.resolve(
    constants.IOC_REGISTER,
    f"{MovingObject.__name__}.location.set",
    lambda obj, attribute, value: SetAttributeValueCommand(
        obj=obj.obj, attribute=attribute, value=value, strategy=DefaultSetPropertyStrategy
    ),
).execute()
IoC.resolve(
    constants.IOC_REGISTER,
    f"{MovingObject.__name__}.velocity.get",
    lambda obj: DefaultGetPropertyStrategy(obj=obj.obj, attribute="velocity").resolve(),
).execute()

session = Session()
response = session.post(url="http://127.0.0.1:5000/api/games/start")


game_id = response.json()["game_id"]
object_id = OBJECTS[0]["object_id"]


message = Message(
    game_id=game_id,
    object_id=object_id,
    operation_id=constants.OPR_MOVING_STRAIGHT_LINE,
    args=Vector(1, 1),
)


response = session.post(
    url="http://127.0.0.1:5000/api/games/messages",
    json=message.model_dump_json(),
)

obj_ = IoC.resolve(constants.GAME_OBJECT, object_id)
print(obj_)
print(adapter.get_velocity())
adapter.set_location(Vector(10, 10))
print(obj_)
print(adapter.get_velocity())

print(InitCommand.root_scope)
"""


"""
OBJECT_1 = {
    "object_id": "1",
    "location": Vector(1, 1)
}

InitCommand().execute()

IoC.resolve(
    constants.IOC_REGISTER,
    f"{constants.GAME_OBJECT}.{OBJECT_1['object_id']}",
    lambda : OBJECT_1
).execute()

IoC.resolve(
    constants.IOC_REGISTER,
    constants.GAME_OBJECT,
    lambda id_: IoC.resolve(f"{constants.GAME_OBJECT}.{id_}")
).execute()
IoC.resolve(IOC_REGISTER, ADAPTER, lambda class_, obj: auto_generate_adapter(class_, obj)).execute()

adapter = IoC.resolve(ADAPTER, MovingObject, OBJECT_1)
print(dir(adapter))
IoC.resolve(
    IOC_REGISTER,
    f"{MovingObject.__name__}.location.set",
    lambda obj, attribute, value: SetAttributeValueCommand(
        obj=obj.obj, attribute=attribute, value=value, strategy=DefaultSetPropertyStrategy
    ),
).execute()

obj_ = IoC.resolve(constants.GAME_OBJECT, 1)
print(OBJECT_1)
print(obj_)
adapter.set_location(Vector(2, 2))
print(obj_)
print(OBJECT_1)


sys.exit(1)

session = Session()

response = session.post(
    url="http://127.0.0.1:5000/api/games/start"
)
print(response.json())



message = Message(
    game_id=response.json()["game_id"],
    object_id="object1",
    operation_id="operation1",
    args={"x": 5, "y": 5},
)


response = session.post(
    url="http://127.0.0.1:5000/api/games/messages",
    json=message.model_dump_json(),
)
print(response.status_code)
print(response.json())
"""
