def test_crud(client,task):
    url=f'/api/v1/tasks/{task}'
    assert client.get(url).status_code==200
    assert client.put(url,json={'title':'Updated'}).json()['title']=='Updated'
    assert client.delete(url).status_code==204
    assert client.get(url).status_code==404
def test_validation(client,project):
    assert client.post(f'/api/v1/projects/{project}/tasks',json={'title':''}).status_code==422
