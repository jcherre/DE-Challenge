SELECT
    b.department,
    c.job,
    COUNT(DISTINCT CASE WHEN TO_CHAR(TO_TIMESTAMP(a.datetime, 'YYYY-MM-DD"T"HH24:MI:SS'), 'MM') IN ('01', '02', '03') THEN a.id END) AS Q1,
    COUNT(DISTINCT CASE WHEN TO_CHAR(TO_TIMESTAMP(a.datetime, 'YYYY-MM-DD"T"HH24:MI:SS'), 'MM') IN ('04', '05', '06') THEN a.id END) AS Q2,
    COUNT(DISTINCT CASE WHEN TO_CHAR(TO_TIMESTAMP(a.datetime, 'YYYY-MM-DD"T"HH24:MI:SS'), 'MM') IN ('07', '08', '09') THEN a.id END) AS Q3,
    COUNT(DISTINCT CASE WHEN TO_CHAR(TO_TIMESTAMP(a.datetime, 'YYYY-MM-DD"T"HH24:MI:SS'), 'MM') IN ('10', '11', '12') THEN a.id END) AS Q4
FROM employees a
LEFT JOIN departments b ON b.id = a.department_id
LEFT JOIN jobs c ON c.id = a.job_id
WHERE TO_CHAR(TO_TIMESTAMP(a.datetime, 'YYYY-MM-DD"T"HH24:MI:SS'), 'YYYY') = '{year}'
AND a.datetime <> 'nan'
GROUP BY 1,2
ORDER BY 1,2