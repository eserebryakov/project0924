import threading
from uuid import uuid4

import pytest
from requests import Session

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.common import constants
from src.spacebattle.common.vector import Vector
from src.spacebattle.core.message import Message
from src.spacebattle.scopes.ioc import IoC
from src.spacebattle.scopes.strategy import _strategy

TEST_OBJECT = {
    "object_id": str(uuid4()),
    "location": Vector(2, 2).model_dump(),
    "velocity": Vector(0, 0).model_dump(),
}


class TestEndpoint:
    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        self.session = Session()
        response = self.session.post(url="http://127.0.0.1:5000/api/games/start")
        self.game_id = response.json()["game_id"]
        self.object_id = TEST_OBJECT["object_id"]

        message = Message(
            game_id=self.game_id,
            object_id=self.object_id,
            operation_id=constants.OPERATION_CREATE_OBJECT,
            args=TEST_OBJECT,
        )
        response = self.session.post(
            url="http://127.0.0.1:5000/api/games/messages",
            json=message.model_dump_json(),
        )

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_endpoint_moving_object(self, initial_state):
        message = Message(
            game_id=self.game_id,
            object_id=self.object_id,
            operation_id=constants.OPERATION_MOVING_STRAIGHT_LINE,
            args=Vector(100, 100),
        )
        response = self.session.post(
            url="http://127.0.0.1:5000/api/games/messages",
            json=message.model_dump_json(),
        )
        print(response.text)
        assert response.json()["args"]["location"] == Vector(102, 102).model_dump()
