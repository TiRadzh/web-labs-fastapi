def test_projects(client,project):
    assert client.get('/api/v1/projects').json()['total']==1
    assert client.get(f'/api/v1/projects/{project}').status_code==200
def test_forbidden(client,project):
    data={'username':'other','password':'password123'}
    client.post('/api/v1/auth/register',json=data)
    client.headers['Authorization']='Bearer '+client.post('/api/v1/auth/login',json=data).json()['access_token']
    assert client.delete(f'/api/v1/projects/{project}').status_code==403
