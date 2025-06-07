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


class TestUnsuccessfulIdentity:
    @pytest.fixture(scope="function")
    def initial_state(self, request):
        InitCommand.root_scope = {}
        InitCommand.current_scope = threading.local()
        InitCommand.already_executed_successfully = False
        IoC.strategy = _strategy
        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value

        self.session = Session()
        self.user_id_1, self.user_id_2, self.user_id_3 = str(uuid4()), str(uuid4()), str(uuid4())
        response = self.session.post(
            url="http://127.0.0.1:5000/api/games/start_sec",
            json={"participants": [self.user_id_1, self.user_id_2, self.user_id_3]},
        )
        self.game_id_1 = response.json()["game_id"]
        response = self.session.post(
            url="http://127.0.0.1:5001/api/auth/token", json={"game_id": self.game_id_1, "user_id": self.user_id_1}
        )
        self.token_1 = response.json()["access_token"]

        self.user_id_4 = str(uuid4())
        response = self.session.post(
            url="http://127.0.0.1:5000/api/games/start_sec",
            json={"participants": [self.user_id_4]},
        )
        self.game_id_2 = response.json()["game_id"]
        response = self.session.post(
            url="http://127.0.0.1:5001/api/auth/token", json={"game_id": self.game_id_2, "user_id": self.user_id_4}
        )
        self.token_2 = response.json()["access_token"]

        self.object_id = TEST_OBJECT["object_id"]

        def teardown():
            InitCommand.root_scope = {}
            InitCommand.current_scope = threading.local()
            InitCommand.already_executed_successfully = False
            IoC.strategy = _strategy
            if hasattr(InitCommand.current_scope, "value"):
                del InitCommand.current_scope.value

        request.addfinalizer(teardown)

    def test_unsuccessful_identity_moving_object(self, initial_state):
        message = Message(
            game_id=self.game_id_1,
            object_id=self.object_id,
            operation_id=constants.OPERATION_CREATE_OBJECT,
            args=TEST_OBJECT,
        )
        response = self.session.post(
            url="http://127.0.0.1:5000/api/games/messages_sec",
            headers={
                "Authorization": "Bearer " + self.token_2,
            },
            json=message.model_dump_json(),
        )
        assert response.status_code == 403
