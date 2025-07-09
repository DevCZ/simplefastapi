from fastapi import FastAPI
import uvicorn


from pydantic import BaseModel

app = FastAPI()

# In-memory user storage
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]

# Pydantic model for user input
class User(BaseModel):
    id: int
    name: str


# GET endpoint: return default 3 users
@app.get("/")
async def root():
    return users




# POST endpoint: create user
@app.post("/")
async def create_item(user: User):
    users.append({"id": user.id, "name": user.name})
    return user



# PUT endpoint: update user by id (replace)
@app.put("/")
async def update_item(user: User):
    for idx, u in enumerate(users):
        if u["id"] == user.id:
            users[idx] = {"id": user.id, "name": user.name}
            return users[idx]
    return {"error": "User not found"}



# PATCH endpoint: update user name by id (partial)
from typing import Optional
class UserPatch(BaseModel):
    id: int
    name: Optional[str] = None

@app.patch("/")
async def patch_item(user: UserPatch):
    for u in users:
        if u["id"] == user.id:
            if user.name is not None:
                u["name"] = user.name
            return u
    return {"error": "User not found"}


# DELETE endpoint: delete user by id
@app.delete("/")
async def delete_item(id: int):
    for idx, u in enumerate(users):
        if u["id"] == id:
            deleted = users.pop(idx)
            return deleted
    return {"error": "User not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
