from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API is running"}


def test_create_task():
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Testing API",
        "priority": "high",
        "completed": False,
        "user_id": 1
    })

    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200


def test_get_task_by_id():
    create_response = client.post("/tasks", json={
        "title": "Get One Task",
        "description": "Testing get one",
        "priority": "medium",
        "completed": False,
        "user_id": 1
    })

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_invalid_task_id():
    response = client.get("/tasks/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task():
    create_response = client.post("/tasks", json={
        "title": "Old Task",
        "description": "Old description",
        "priority": "low",
        "completed": False,
        "user_id": 1
    })

    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Task",
        "description": "Updated description",
        "priority": "high",
        "completed": False,
        "user_id": 1
    })

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"


def test_complete_task():
    create_response = client.post("/tasks", json={
        "title": "Complete Task",
        "description": "Testing complete",
        "priority": "high",
        "completed": False,
        "user_id": 1
    })

    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task():
    create_response = client.post("/tasks", json={
        "title": "Delete Task",
        "description": "Testing delete",
        "priority": "low",
        "completed": False,
        "user_id": 1
    })

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}
    