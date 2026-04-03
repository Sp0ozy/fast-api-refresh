from fastapi import status
from .utils import *
from ..models import Todos
from ..routers.auth import get_current_user
from ..routers.todos import get_db
from ..main import app

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
    
def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": test_todo.id,
                                "title": "Test Todo",
                                "description": "Test Description",
                                "priority": 5,
                                "complete": False,
                                "owner_id": 1}]

def test_read_one_authenticated(test_todo):
    response = client.get(f"/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": test_todo.id,
                               "title": "Test Todo",
                               "description": "Test Description",
                               "priority": 5,
                               "complete": False,
                               "owner_id": 1}

def test_read_one_authenticated_not_found(test_todo):
    response = client.get(f"/todo/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
    
def test_create_todo_authenticated(test_user):
    request_body = {"title": "New Todo", "description": "New Description", "priority": 3, "complete": False}
    response = client.post("/todo", json=request_body)
    assert response.status_code == status.HTTP_201_CREATED
    db=TestSessionLocal()
    todo_model = db.query(Todos).filter(Todos.title == "New Todo").first()
    assert todo_model is not None
    assert todo_model.description == "New Description"
    assert todo_model.priority == 3
    assert todo_model.complete == False
    assert todo_model.owner_id == 1

def test_update_todo_authenticated(test_todo):
    request_body = {"title": "Updated Todo", "description": "Updated Description", "priority": 1, "complete": True}
    response = client.put(f"/todo/{test_todo.id}", json=request_body)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert todo_model is not None
    assert todo_model.title == "Updated Todo"
    assert todo_model.description == "Updated Description"
    assert todo_model.priority == 1
    assert todo_model.complete == True

def test_update_todo_authenticated_not_found():
    request_body = {"title": "Updated Todo", "description": "Updated Description", "priority": 1, "complete": True}
    response = client.put(f"/todo/9999", json=request_body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

def test_delete_todo_authenticated(test_todo):
    response = client.delete(f"/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert todo_model is None

def test_delete_todo_authenticated_not_found():
    response = client.delete(f"/todo/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
