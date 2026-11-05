import os
import asyncpg

# Если есть DATABASE_URL (как на Render), используем её. Иначе берем по кусочкам (как локально).
DB_URL = os.getenv("DATABASE_URL")

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        if DB_URL:
            # Render дает ссылку вида postgres://user:pass@host/db
            # asyncpg требует postgresql://, поэтому меняем префикс
            dsn = DB_URL.replace("postgres://", "postgresql://")
            _pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=10)
        else:
            # Локальный запуск (в Docker)
            _pool = await asyncpg.create_pool(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                host=os.getenv("DB_HOST", "db"),
                port=os.getenv("DB_PORT", "5432"),
                min_size=1,
                max_size=10,
            )
    return _pool

async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None