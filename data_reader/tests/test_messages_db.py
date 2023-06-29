from http import HTTPStatus


def test_messages_db(mock_open, client_db):
    response = client_db.get("/messages_db")
    assert response.status_code == HTTPStatus.OK
    assert response.text == ('[]')


def test_messages_db_offset_imit(mock_open, client_db):
    response = client_db.get("/messages_db?offset=20&limit=1")
    assert response.status_code == HTTPStatus.OK
    assert response.text == ('[]')


def test_messages_db_offset(mock_open, client_db):
    response = client_db.get("/messages_db?offset=20")
    assert response.status_code == HTTPStatus.OK
    assert response.text == ('[]')


def test_messages_db_imit(mock_open, client_db):
    response = client_db.get("/messages_db?limit=1")
    assert response.status_code == HTTPStatus.OK
    assert response.text == ('[]')