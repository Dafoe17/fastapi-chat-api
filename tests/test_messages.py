from fastapi import status


def test_send_message(test_client):
    chat = test_client.post("/chats/", json={"title": "Message Chat"}).json()
    chat_id = chat["id"]

    response = test_client.post(f"/chats/{chat_id}/messages/", json={"text": "Hello"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["text"] == "Hello"
    assert "id" in data
    assert data["chat_id"] == chat_id


def test_chat_title_validation(test_client):
    chat = test_client.post("/chats/", json={"title": "Message Chat"}).json()
    chat_id = chat["id"]

    response = test_client.post(
        f"/chats/{chat_id}/messages/", json={"text": "A" * 5001}
    )
    assert response.status_code == 422

    response = test_client.post(f"/chats/{chat_id}/messages/", json={"text": ""})
    assert response.status_code == 422


def test_message_not_existing(test_client):
    response = test_client.post("/chats/9999/messages/", json={"text": "Test"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
