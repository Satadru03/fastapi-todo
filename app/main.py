#my_env\Scripts\activate
#uvicorn main:app --reload

#docker build -t fastapi-todo .
#docker images
#docker run -p 8000:8000 fastapi-todo

#http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException, Depends, Request
from schema import UserCreate, UserResponse, UserUpdate, APIResponse, Token, TodoCreate, TodoResponse, TodoUpdate
from typing import List
from db import get_db_connection
import crud
from auth import hash_password, verify_password, create_access_token
from auth import get_current_user
from fastapi.responses import JSONResponse
from time import time
import logging_config
from logging_config import logger

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled error: {request.method} {request.url.path}")
        raise
    duration = time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {duration:.2f}s"
    )

    return response

def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()

@app.get("/me")
def read_me(current_user: str = Depends(get_current_user)): 
    return {"username": current_user}

@app.post("/users", response_model = APIResponse, status_code = 201)
def create_user_api(user: UserCreate, db = Depends(get_db)):
    if user.age < 13:
        raise HTTPException(status_code=400, detail="User too young")

    password_hash = hash_password(user.password)
    
    result = crud.create_user(db, user, password_hash)
    if result is None:
        raise HTTPException(status_code=409, detail="User already exists")

    return {
        "status": "success",
        "message": "User created",
        "data": result
    }

@app.get("/users", response_model = List[UserResponse])
def get_all_users_api(db = Depends(get_db)):
    return crud.get_all_users(db)

@app.get("/user/{username}", response_model = UserResponse)
def get_user_api(username: str, db = Depends(get_db)):
    result = crud.get_user(db, username)
    if result is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return result

@app.put("/users/{username}", response_model = UserResponse)
def update_user_api(username: str, user_update: UserUpdate, db = Depends(get_db)):
    result = crud.update_user(db, username, user_update)
    if result is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return result

@app.post("/login", response_model = Token)
def login_api(username: str, password: str, db = Depends(get_db)):
    result = crud.login(db, username)
    if not verify_password(password, result):
        raise HTTPException(status_code = 401, detail = "Invalid password")
    
    token = create_access_token({"sub": username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.delete("/users/{username}")
def delete_user_api(username: str, db = Depends(get_db)):
    result = crud.delete_user(db, username)
    if result is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return {
        "status": "success",
        "message": "User deleted"
    }

@app.post("/todos", response_model = TodoResponse) 
def create_todos_api(todo: TodoCreate, current_user: str = Depends(get_current_user), db = Depends(get_db)):
    return crud.create_todos(db, current_user, todo.title)

@app.get("/todos", response_model = List[TodoResponse])
def get_todos_api(current_user: str = Depends(get_current_user), db = Depends(get_db)):
    todos = crud.get_todos(db, current_user)
    return todos

@app.put("/todos", response_model = TodoResponse)
def update_todo_api(id: int, todo_update: TodoUpdate, current_user: str = Depends(get_current_user), db = Depends(get_db)):
    result = crud.update_todos(db, id, current_user, todo_update)

    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")

    return result

@app.delete("/todos/{id}")
def delete_todo_api(id: int, current_user: str = Depends(get_current_user), db = Depends(get_db)):
    result = crud.delete_todos(db, current_user, id)

    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted"}
