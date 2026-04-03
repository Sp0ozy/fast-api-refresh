from .utils import *
from ..routers.user import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'first_name': test_user.first_name,
                               'username': test_user.username,
                               'email': test_user.email,
                               'last_name': test_user.last_name,
                               'is_active': test_user.is_active,
                               'phone_number': test_user.phone_number,
                               'id': test_user.id,
                               'hashed_password': test_user.hashed_password,
                               'role': test_user.role}

def test_change_password_success(test_user):
    request_body = {"password": "password", "new_password": "newpassword"}
    response = client.put("/user", json=request_body)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestSessionLocal()
    user_model = db.query(Users).filter(Users.id == test_user.id).first()
    assert user_model is not None
    assert bcrypt_context.verify("newpassword", user_model.hashed_password)
    
def test_change_password_invalid_password(test_user):
    request_body = {"password": "wrongpassword", "new_password": "newpassword"}
    response = client.put("/user", json=request_body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid password"}

def test_change_phone_number(test_user):
    new_phone_number = "1234567890"
    response = client.put(f"/user/phone_number/{new_phone_number}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestSessionLocal()
    user_model = db.query(Users).filter(Users.id == test_user.id).first()
    assert user_model is not None
    assert user_model.phone_number == new_phone_number