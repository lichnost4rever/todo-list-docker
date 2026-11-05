# Todo API — практическая работа по Docker

## Стек
- Python 3.12 + FastAPI
- PostgreSQL 16
- Docker Compose

## Структура
- `app/` — FastAPI-приложение
- `db/` — SQL-инициализация БД
- `docker-compose.yml` — оркестрация

## Запуск
1. Заполнить `.env` (по образцу `.env.example`)
2. `docker compose up --build`
3. Swagger: http://localhost:8080/docs

## Эндпоинты
| Метод  | URL            | Описание |
|--------|----------------|----------|
| POST   | /tasks         | Создать |
| GET    | /tasks         | Все |
| GET    | /tasks/{id}    | Одну |
| PUT    | /tasks/{id}    | Обновить |
| DELETE | /tasks/{id}    | Удалить |
| GET    | /health        | Проверка |

## Архитектура
- `api` — контейнер с FastAPI, порт 8080 проброшен наружу
- `db` — контейнер с Postgres, доступен только внутри сети `backend`
- Volume `db_data` — хранение данных БД