from fastapi import FastAPI, HTTPException, Depends,Query,Header
from pydantic import BaseModel
from typing import List, Annotated


app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    
tasks: List[Task] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task API!"}


def authenticate(token:str = Header(...)):
    if token != "secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    

@app.get("/tasks",response_model=List[Task])
def get_tasks(completed: bool= Query(None)):
    if completed is not None:
        return [task for task in tasks if task.completed == completed]
    return tasks


# get a specific task by id
@app.get("/tasks/{task_id}", response_model=Task, dependencies=[Depends(authenticate)])
def get_task(task_id:int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")
                  
# create a new task
@app.post("/tasks",response_model=List[Task], dependencies=[Depends(authenticate)])
def create_task(task_list:List[Task]):
    for task in task_list:
      task.id = len(tasks) + 1
      tasks.append(task)
    return task_list   

# update the task
@app.put("/tasks/{task_id}", response_model=Task, dependencies=[Depends(authenticate)])
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task.id = task_id
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")


# delete a task
@app.delete("/tasks/{task_id}", dependencies=[Depends(authenticate)])
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"detail": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")        