def test_me(client,auth):
    assert client.get('/api/v1/users/me').json()['id']==auth['id']
