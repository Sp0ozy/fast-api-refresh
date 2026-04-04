from fastapi import FastAPI, Request
from .models import Base
from .database import engine
from .routers import auth, todos, admin, user
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import status
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="todo/static"), name="static")

@app.get("/", status_code=200)
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/health", status_code=200)
def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)

