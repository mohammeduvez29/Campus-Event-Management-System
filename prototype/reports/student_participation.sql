SELECT students.name, COUNT(a.id) AS attended_events
FROM students
LEFT JOIN attendance a ON students.id = a.student_id
GROUP BY students.id
ORDER BY attended_events DESC;
