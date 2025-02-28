with hirings AS (
    SELECT
        b.id,
        b.department,
        TO_CHAR(TO_TIMESTAMP(a.datetime, 'YYYY-MM-DD"T"HH24:MI:SS'), 'YYYY')  AS year_hired,
        COUNT(DISTINCT a.id) as hired
    FROM employees a
    LEFT JOIN departments b ON b.id = a.department_id
    WHERE a.datetime <> 'nan'
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