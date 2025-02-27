SELECT
    b.department,
    c.job,
    COUNT(DISTINCT CASE WHEN strftime('%m', a.datetime) IN ('01', '02', '03') THEN a.id END) AS Q1,
    COUNT(DISTINCT CASE WHEN strftime('%m', a.datetime) IN ('04', '05', '06') THEN a.id END) AS Q2,
    COUNT(DISTINCT CASE WHEN strftime('%m', a.datetime) IN ('07', '08', '09') THEN a.id END) AS Q3,
    COUNT(DISTINCT CASE WHEN strftime('%m', a.datetime) IN ('10', '11', '12') THEN a.id END) AS Q4
FROM employees a
LEFT JOIN departments b ON b.id = a.department_id
LEFT JOIN jobs c ON c.id = a.job_id
WHERE strftime('%Y', a.datetime) = '{year}'
GROUP BY 1,2
ORDER BY 1,2