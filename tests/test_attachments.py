def test_upload(client,task):
    url=f'/api/v1/tasks/{task}/attachments'
    r=client.post(url,files={'file':('a.txt',b'hello','text/plain')})
    assert r.status_code==201
    path='/api/v1/attachments/'+str(r.json()['id'])
    assert client.get(path).content==b'hello'
    assert client.delete(path).status_code==204
    assert client.post(url,files={'file':('a.exe',b'x','application/octet-stream')}).status_code==415
