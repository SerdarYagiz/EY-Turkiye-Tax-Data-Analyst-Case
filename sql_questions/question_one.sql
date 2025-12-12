SELECT
    t.team_name,
    COUNT(*) AS resolved_ticket_count
FROM tickets tk
JOIN teams t ON t.team_id = tk.team_id
WHERE
    tk.resolution_date IS NOT NULL
    AND tk.resolution_date <= tk.ticket_date + INTERVAL '7 days'
GROUP BY t.team_name
HAVING COUNT(*) > 100;
