SET client_encoding = 'UTF8';

-- Таблица комнат
CREATE TABLE IF NOT EXISTS rooms (
    id      INTEGER PRIMARY KEY,
    name    VARCHAR(50) NOT NULL UNIQUE
);

-- Таблица студентов
CREATE TABLE IF NOT EXISTS students (
    id        INTEGER PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    birthday  TIMESTAMP NOT NULL,
    sex       CHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
    room      INTEGER NOT NULL REFERENCES rooms(id) ON DELETE RESTRICT
);

-- Индексы для оптимизации аналитических запросов
-- 1. Для JOIN и GROUP BY по комнатам
CREATE INDEX IF NOT EXISTS idx_students_room ON students(room);

-- 2. Для вычисления возраста и сортировок (покрывающий индекс)
CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);

-- 3. Составной индекс для запроса "разнополые студенты"
CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room, sex);