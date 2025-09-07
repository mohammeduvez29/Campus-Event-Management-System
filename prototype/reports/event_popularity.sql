SELECT events.name, COUNT(r.id) AS registrations
FROM events
LEFT JOIN registrations r ON events.id = r.event_id
GROUP BY events.id
ORDER BY registrations DESC;
