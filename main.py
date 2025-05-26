from fastapi import FastAPI, Depends, HTTPException, Query, Header
from pydantic import BaseModel
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Task model using Pydantic
class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False

# In-memory storage for tasks (list)
tasks: List[Task] = []

# Dependency for basic authentication (checks for a token in headers)
def authenticate(token: str = Header(...)):
    if token != "mysecrettoken":
        raise HTTPException(status_code=401, detail="Unauthorized")

# GET /tasks - Retrieve all tasks or filtered tasks
@app.get("/tasks", response_model=List[Task])
def get_tasks(completed: bool = Query(None)):
    if completed is not None:
        return [task for task in tasks if task.completed == completed]
    return tasks

# GET /tasks/{task_id} - Retrieve a specific task
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# POST /tasks - Create a new task (requires authentication)
@app.post("/tasks", response_model=List[Task], dependencies=[Depends(authenticate)])
def create_task(task_list: List[Task]):
    # Assign a new ID based on the current length of the tasks list
    for task in task_list:
        task.id == len(tasks) + 1
        tasks.append(task)
    return tasks

# PUT /tasks/{task_id} - Update a task (requires authentication)
@app.put("/tasks/{task_id}", response_model=Task, dependencies=[Depends(authenticate)])
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task.id = task_id
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE /tasks/{task_id} - Delete a task (requires authentication)
@app.delete("/tasks/{task_id}", dependencies=[Depends(authenticate)])
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"detail": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


