from email.mime import message
from http import client
from readline import append_history_file
from urllib import response
from fastapi.testclient import TestClient

from main import app

client=TestClient(app)

def test_get_all_blogs():
    response=client.get("/blog/all")
    assert response.status_code ==200

def test_auth_error():
    response=client.post("/token",data={'username':'mahabub','password':'mahabub'})
    access_token=response.json().get("access_token")
    assert access_token==None
    message=response.json().get("detail")[0].get('msg')
    assert message=="field Required"
    
def test_auth_sucess():
    response=client.post("/token",data={'username':'','password':''})
    access_token=response.json().get("access_token")
    assert access_token==None

def test_post_article():
    auth=client.post('/token',data={'username':'mahabub','password':'mahabub'})
    access_token=auth.json().get("access_token")
    assert access_token

    respone=client.post(
        "/article/",
        json={"title":"test","content":"test content","published":True,"creator_id":1},
        header={
            "Authorization":"bearer"+access_token
        }
    )
    assert response.status_code ==200
    assert response.json().get("title")=="test"

