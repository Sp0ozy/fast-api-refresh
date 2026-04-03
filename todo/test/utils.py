import os
from xmlrpc import client
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from ..models import Todos,Users
from ..database import Base
from ..main import app
from ..routers.auth import bcrypt_context


load_dotenv('todo/.env')

SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username": "bob", "id": 1, "user_role": "admin"}
        

client = TestClient(app)

@pytest.fixture
def test_todo(test_user):
    todo=Todos(title="Test Todo", description="Test Description", priority=5, complete=False, owner_id=test_user.id)

    db=TestSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as connection:
        connection.execute(text("TRUNCATE TABLE todos RESTART IDENTITY"))
        connection.commit()

@pytest.fixture
def test_user():
    with engine.connect() as connection:
        connection.execute(text("TRUNCATE TABLE todos, users RESTART IDENTITY CASCADE"))
        connection.commit()

    user=Users(username="bob", email="bob@bob", first_name="bob", last_name="bob", hashed_password=bcrypt_context.hash("password"), role="admin")

    db=TestSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    with engine.connect() as connection:
        connection.execute(text("TRUNCATE TABLE todos, users RESTART IDENTITY CASCADE"))
        connection.commit()