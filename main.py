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
    return {"users": users}



# POST endpoint: create user
@app.post("/")
async def create_item(user: User):
    users.append({"id": user.id, "name": user.name})
    return {"message": "User created", "user": {"id": user.id, "name": user.name}}


# PUT endpoint: update user by id (replace)
@app.put("/")
async def update_item(user: User):
    for idx, u in enumerate(users):
        if u["id"] == user.id:
            users[idx] = {"id": user.id, "name": user.name}
            return {"message": "User updated", "user": {"id": user.id, "name": user.name}}
    return {"message": "User not found"}


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
            return {"message": "User patched", "user": u}
    return {"message": "User not found"}

# DELETE endpoint
@app.delete("/")
async def delete_item():
    return {"message": "DELETE request received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
