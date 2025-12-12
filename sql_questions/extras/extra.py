import pandas as pd
import sqlite3

files = {
    "teams": "teams.csv",
    "tickets": "tickets.csv",
    "clients": "clients.csv"
}

conn = sqlite3.connect("mydb.sqlite")

for table_name, file_path in files.items():
    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)

# SQL Question 1
# Write a SQL query to find the teams that have resolved more than 100 tickets in total. Include only those tickets that were resolved within 7 days of their creation.

sql1 = """
SELECT
    t.team_id,
    tm.team_name,
    COUNT(*) AS total_resolved
FROM tickets t
JOIN teams tm ON t.team_id = tm.team_id
WHERE t.resolution_date IS NOT NULL
  AND DATE(t.resolution_date) <= DATE(t.ticket_date, '+7 day')
GROUP BY t.team_id, tm.team_name
HAVING COUNT(*) > 100;
"""

df1 = pd.read_sql_query(sql1, conn)
print("\n--- SQL Question 1 Results ---")
print(df1)

# SQL Question 2
# Write a SQL query to find the average time taken to resolve tickets by each team. Use a common table expression (CTE) to 
# first calculate the time difference between ticket creation and resolution

sql2 = """
WITH diff AS (
    SELECT
        t.team_id,
        tm.team_name,
        (strftime('%s', t.resolution_date) - strftime('%s', t.ticket_date)) / 86400.0 AS diff_days
    FROM tickets t
    JOIN teams tm ON t.team_id = tm.team_id
    WHERE t.resolution_date IS NOT NULL
)
SELECT
    team_id,
    team_name,
    AVG(diff_days) AS avg_resolution_days
FROM diff
GROUP BY team_id, team_name;
"""

df2 = pd.read_sql_query(sql2, conn)
print("\n--- SQL Question 2 Results ---")
print(df2)

# SQL Question 3
# Write a SQL query to calculate the total number of tickets opened by each team 
# (Field Team, BA Team, Tech Support Team) and the cumulative count of tickets for each team over time

sql3 = """
SELECT
    d1.team_id,
    d1.team_name,
    d1.date,
    d1.daily_ticket_count,
    (
        SELECT SUM(d2.daily_ticket_count)
        FROM (
            SELECT
                t.team_id,
                tm.team_name,
                DATE(t.ticket_date) AS date,
                COUNT(*) AS daily_ticket_count
            FROM tickets t
            JOIN teams tm ON t.team_id = tm.team_id
            GROUP BY t.team_id, tm.team_name, DATE(t.ticket_date)
        ) AS d2
        WHERE d2.team_id = d1.team_id
          AND d2.date <= d1.date
    ) AS cumulative_ticket_count
FROM (
    SELECT
        t.team_id,
        tm.team_name,
        DATE(t.ticket_date) AS date,
        COUNT(*) AS daily_ticket_count
    FROM tickets t
    JOIN teams tm ON t.team_id = tm.team_id
    GROUP BY t.team_id, tm.team_name, DATE(t.ticket_date)
) AS d1
ORDER BY d1.team_id, d1.date;
"""

df3 = pd.read_sql_query(sql3, conn)
print("\n--- SQL Question 3 Results ---")
print(df3)

with pd.ExcelWriter("SQL_Question_Results_excel.xlsx", engine="openpyxl") as writer:
    df1.to_excel(writer, sheet_name="QuestionResult1", index=False)
    df2.to_excel(writer, sheet_name="QuestionResult2", index=False)
    df3.to_excel(writer, sheet_name="QuestionResult3", index=False)


conn.close()