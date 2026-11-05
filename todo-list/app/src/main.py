from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from db import close_pool
from models import Task, TaskCreate, TaskUpdate
from crud import create_task, get_all_tasks, get_task, update_task, delete_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_pool()


app = FastAPI(
    title="Todo API",
    description="Практическая работа по Docker",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=201)
async def api_create_task(task: TaskCreate):
    return await create_task(task)


@app.get("/tasks", response_model=list[Task])
async def api_get_tasks():
    try:
        return await get_all_tasks()
    except Exception as e:
        # Этот код выведет ошибку прямо в браузер
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_id}", response_model=Task)
async def api_get_task(task_id: int):
    task = await get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def api_update_task(task_id: int, task: TaskUpdate):
    updated = await update_task(task_id, task)
    if not updated:
        raise HTTPException(404, "Task not found")
    return updated


@app.delete("/tasks/{task_id}", status_code=204)
async def api_delete_task(task_id: int):
    if not await delete_task(task_id):
        raise HTTPException(404, "Task not found")