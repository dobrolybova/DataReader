from http import HTTPStatus

import asynctest


def fake_open_mock(mock):
    fake_open = asynctest.MagicMock()
    fake_open.return_value.__aenter__ = asynctest.CoroutineMock(return_value=mock())
    fake_open.return_value.__aexit__ = asynctest.CoroutineMock()
    return fake_open


def test_messages_file(mock_open, client_file):
    with asynctest.patch("aiofiles.open", new=fake_open_mock(mock_open), scope=asynctest.LIMITED):
        response = client_file.get("/messages_file")
        assert response.status_code == HTTPStatus.OK
        assert response.text == ('{"items":[{"component":"Voomm Output '
                                 'Bracket","country":"Namibia","description":"dolorem hic autem '
                                 'ut.","model":"y0c 2"},{"component":"Eadel Disc '
                                 'Tuner","country":"Macau","description":"sit quia perspiciatis '
                                 'cumque.","model":"ei 2"}],"total":2,"limit":50,"offset":0}')


def test_messages_file_offset(mock_open, client_file):
    with asynctest.patch("aiofiles.open", new=fake_open_mock(mock_open), scope=asynctest.LIMITED):
        response = client_file.get("/messages_file?offset=20")
        assert response.status_code == HTTPStatus.OK
        assert response.text == '{"items":[],"total":2,"limit":50,"offset":20}'


def test_messages_file_limit(mock_open, client_file):
    with asynctest.patch("aiofiles.open", new=fake_open_mock(mock_open), scope=asynctest.LIMITED):
        response = client_file.get("/messages_file?limit=1")
        assert response.status_code == HTTPStatus.OK
        assert response.text == ('{"items":[{"component":"Voomm Output '
                                 'Bracket","country":"Namibia","description":"dolorem hic autem '
                                 'ut.","model":"y0c 2"}],"total":2,"limit":1,"offset":0}')
