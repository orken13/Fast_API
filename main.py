from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

app=FastAPI()


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
# ── In-memory database ───────────────────────────

USERS: dict[int, dict] = {
    1: {"id": 1, "name": "Emel", "email": "emel@example.com", "password": "1234"},
    2: {"id": 2, "name": "Alice", "email": "alice@example.com", "password": "5678"},
}
next_id = 3

# ── Endpoints ────────────────────────────────────
@app.get("/users", response_model=list[UserResponse])
def get_users():
    # Return all users without passwords
    return list(USERS.values())

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    global next_id
    new_user = {"id": next_id, "name": user.name, "email": user.email, "password": user.password}
    USERS[next_id] = new_user
    next_id += 1
    return new_user
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.name:
        user["name"] = data.name
    if data.email:
        user["email"] = data.email
    return user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    del USERS[user_id]
    return {"message": f"User {user_id} deleted"}