import pytest
from fastapi import status


@pytest.mark.parametrize("title", ["First Chat", "Second Chat"])
def test_create_chat(test_client, title):
    response = test_client.post("/chats/", json={"title": title})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == title
    assert "id" in data


@pytest.mark.parametrize("title", ["", "A" * 201, "  Chat  "])
def test_chat_title_validation(test_client, title):
    response = test_client.post("/chats/", json={"title": title})
    if title.strip() == "" or len(title) > 200:
        assert response.status_code == 422
    else:
        assert response.status_code == 200


def test_create_chat_empty_title(test_client):
    response = test_client.post("/chats/", json={"title": ""})
    assert response.status_code == 422


def test_get_chat_with_messages(test_client):
    chat_resp = test_client.post("/chats/", json={"title": "Chat for Messages"})
    chat = chat_resp.json()
    chat_id = chat["id"]

    for i in range(5):
        test_client.post(f"/chats/{chat_id}/messages/", json={"text": f"msg {i}"})

    response = test_client.get(f"/chats/{chat_id}?limit=3")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["messages"]) == 3
    assert data["messages"][0]["text"] == "msg 2"
    assert data["messages"][-1]["text"] == "msg 4"


def test_delete_chat(test_client):
    chat = test_client.post("/chats/", json={"title": "To Delete"}).json()
    chat_id = chat["id"]

    response = test_client.delete(f"/chats/{chat_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get(f"/chats/{chat_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
