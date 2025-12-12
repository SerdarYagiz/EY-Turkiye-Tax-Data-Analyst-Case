WITH ticket_resolution_time AS (
    SELECT
        tk.ticket_id,
        tk.team_id,
        (tk.resolution_date - tk.ticket_date) AS resolution_days
    FROM tickets tk
    WHERE tk.resolution_date IS NOT NULL
)
SELECT
    t.team_name,
    AVG(resolution_days) AS avg_resolution_days
FROM ticket_resolution_time trt
JOIN teams t ON t.team_id = trt.team_id
GROUP BY t.team_name;
