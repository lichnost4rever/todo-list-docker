from db import get_pool
from models import TaskCreate, TaskUpdate


async def create_task(task: TaskCreate):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO tasks (title, description, priority, due_date, done)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
            """,
            task.title, task.description, task.priority, task.due_date, task.done,
        )
    return dict(row)


async def get_all_tasks():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM tasks ORDER BY id")
    return [dict(r) for r in rows]


async def get_task(task_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    return dict(row) if row else None


async def update_task(task_id: int, task: TaskUpdate):
    pool = await get_pool()
    data = task.model_dump(exclude_unset=True)
    if not data:
        return await get_task(task_id)

    set_parts = []
    values = []
    for i, (key, value) in enumerate(data.items(), start=1):
        set_parts.append(f"{key} = ${i}")
        values.append(value)

    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(set_parts)} WHERE id = ${len(values)} RETURNING *"

    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, *values)
    return dict(row) if row else None


async def delete_task(task_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM tasks WHERE id = $1", task_id)
    return result == "DELETE 1"