from .utils import *
from ..routers.auth import get_current_user, get_db, authenticate_user, create_access_token
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException,status

load_dotenv('todo/.env')

app.dependency_overrides[get_db] = override_get_db

def test_authernticate_user(test_user):
    db=TestSessionLocal()
    
    user = authenticate_user(test_user.username, "password", db)
    
    assert user is not None
    assert user.username == test_user.username
    
    non_existent_user = authenticate_user("nonexistent", "password", db)
    assert non_existent_user is None
    
    wrong_password_user = authenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password_user is False
    
def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(minutes=30)

    token = create_access_token(username, user_id, role, expires_delta)
    assert token is not None
    assert isinstance(token, str)
    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role

@pytest.mark.asyncio
async def test_get_current_user_valid():
    encode = {'sub': "bob", 'id': 1, 'role': "admin"}
    token = jwt.encode(encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    
    user = await get_current_user(token=token)
    assert user == {"username": "bob", "id": 1, "user_role": "admin"}
    

@pytest.mark.asyncio
async def test_get_current_user_invalid():
    invalid_token = {"role": "user"}
    token = jwt.encode(invalid_token, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)
        
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"