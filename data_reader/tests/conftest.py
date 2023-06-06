import asynctest
import pytest
from fastapi.testclient import TestClient

from config import Storage, AppSettings
from main import Application


@pytest.fixture()
def srv_file():
    settings = AppSettings(STORAGE=Storage.FILE.name)
    app = Application(settings).app
    return app


@pytest.fixture()
def client_file() -> TestClient:
    settings = AppSettings()
    settings.STORAGE = Storage.FILE.name
    return TestClient(Application(settings).app)


@pytest.fixture(scope="function")
def mock_open():
    def prepare_open():
        fake_open = asynctest.CoroutineMock()
        fake_open.return_value.__bool__ = True
        fake_open.read = asynctest.CoroutineMock(return_value="{'component': 'Voomm Output Bracket', 'country': "
                                                              "'Namibia', 'description': 'dolorem hic autem ut.', "
                                                              "'model': 'y0c 2'}\n{'component': 'Eadel Disc Tuner', "
                                                              "'country': 'Macau', 'description': 'sit quia "
                                                              "perspiciatis cumque.', 'model': 'ei 2'}\n")

        return fake_open

    return prepare_open
