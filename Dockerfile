# Используем официальный образ Python 3.12 (совпадает с твоим venv)
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и устанавливаем их
# Делаем это ДО копирования кода, чтобы использовать кэш Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY src/ ./src/
COPY config/ ./config/

# Точка входа: запуск CLI через модуль
# Аргументы (--students, --rooms, --format) передаются при docker compose run
ENTRYPOINT ["python", "-m", "src.cli"]