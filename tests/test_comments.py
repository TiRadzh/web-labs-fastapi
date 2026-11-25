def test_comment(client,task,auth):
    url=f'/api/v1/tasks/{task}/comments'
    assert client.post(url,json={'text':'Hello','user_id':auth['id']}).status_code==201
    assert len(client.get(url).json())==1
