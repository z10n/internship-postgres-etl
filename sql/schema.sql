SET client_encoding = 'UTF8';

CREATE TABLE IF NOT EXISTS rooms (
    id      INTEGER PRIMARY KEY,
    name    VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS students (
    id        INTEGER PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    birthday  TIMESTAMP NOT NULL,
    sex       CHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
    room      INTEGER NOT NULL REFERENCES rooms(id) ON DELETE RESTRICT
);

-- Indexes for optimizing analytical queries
-- 1. Optimizes JOINs and GROUP BY on room
CREATE INDEX IF NOT EXISTS idx_students_room ON students(room);

-- 2. Optimizes age calculation and sorting
CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);

-- 3. Composite index for the "mixed sex rooms" query
CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room, sex);