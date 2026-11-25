def test_register_login(client):
    data={'username':'new','password':'password123'}
    assert client.post('/api/v1/auth/register',json=data).status_code==201
    assert 'access_token' in client.post('/api/v1/auth/login',json=data).json()
def test_unauthorized(client):
    assert client.get('/api/v1/users/me').status_code==401
