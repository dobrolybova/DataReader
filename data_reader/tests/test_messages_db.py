from http import HTTPStatus


# TODO: Test is failed
def test_messages_db(mock_open, client_db):
    response = client_db.get("/messages_db")
    assert response.status_code == HTTPStatus.OK
    assert response.text == ('{"items":[{"component":"Voomm Output '
                             'Bracket","country":"Namibia","description":"dolorem hic autem '
                             'ut.","model":"y0c 2"},{"component":"Eadel Disc '
                             'Tuner","country":"Macau","description":"sit quia perspiciatis '
                             'cumque.","model":"ei 2"}],"total":2,"limit":50,"offset":0}')
