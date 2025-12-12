SELECT
    t.team_name,
    tk.ticket_date,
    COUNT(*) AS tickets_opened_on_day,
    SUM(COUNT(*)) OVER (
        PARTITION BY t.team_name
        ORDER BY tk.ticket_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_ticket_count
FROM tickets tk
JOIN teams t ON t.team_id = tk.team_id
GROUP BY
    t.team_name,
    tk.ticket_date;
