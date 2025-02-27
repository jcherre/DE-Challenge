with hirings AS (
    SELECT
        b.id,
        b.department,
        strftime('%Y', a.datetime) AS year_hired,
        COUNT(DISTINCT a.id) as hired
    FROM employees a
    LEFT JOIN departments b ON b.id = a.department_id
    GROUP BY 1,2,3
)
SELECT
    id,
    department,
    SUM(hired) as hired
FROM hirings
GROUP BY 1,2
HAVING SUM(hired) > (SELECT AVG(hired) FROM hirings WHERE year_hired = '{year}')
ORDER BY SUM(hired) desc