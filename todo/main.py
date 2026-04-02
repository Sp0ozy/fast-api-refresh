from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos, admin, user

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health", status_code=200)
async def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)

