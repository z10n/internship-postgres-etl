-- 1. Количество студентов в каждой комнате
SELECT r.name AS room_name, COUNT(s.id) AS student_count
FROM rooms r
LEFT JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
ORDER BY r.name;

-- 2. Топ-5 комнат с минимальным средним возрастом
SELECT r.name AS room_name, 
       AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) AS avg_age
FROM rooms r
JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
ORDER BY avg_age ASC
LIMIT 5;

-- 3. Топ-5 комнат с максимальной разницей в возрасте
SELECT r.name AS room_name,
       MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) - 
       MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) AS age_diff
FROM rooms r
JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
ORDER BY age_diff DESC
LIMIT 5;

-- 4. Комнаты с разнополыми студентами
SELECT r.name AS room_name
FROM rooms r
JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
HAVING COUNT(DISTINCT s.sex) > 1
ORDER BY r.name;