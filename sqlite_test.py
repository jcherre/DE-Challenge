import sqlite3
import csv

conn = sqlite3.connect('instance/local.db')
cur = conn.cursor()

""" cur.execute("DELETE FROM departments")
cur.execute("DELETE FROM jobs")
cur.execute("DELETE FROM employees")
# Commit the transaction
conn.commit() """

#cur.execute("SELECT * FROM departments")
#print(cur.fetchall())
#cur.execute("SELECT * FROM jobs")
#print(cur.fetchall())
#cur.execute("SELECT * FROM employees")
#print(cur.fetchall())
cur.execute("""SELECT
    b.department,
    c.job,
    COUNT(DISTINCT CASE WHEN strftime('%m', a.datetime) IN ('01', '02', '03') THEN a.id END) AS Q1,
    COUNT(DISTINCT CASE WHEN strftime('%m', a.datetime) IN ('04', '05', '06') THEN a.id END) AS Q2,
    COUNT(DISTINCT CASE WHEN strftime('%m', a.datetime) IN ('07', '08', '09') THEN a.id END) AS Q3,
    COUNT(DISTINCT CASE WHEN strftime('%m', a.datetime) IN ('10', '11', '12') THEN a.id END) AS Q4
FROM employees a
LEFT JOIN departments b ON b.id = a.department_id
LEFT JOIN jobs c ON c.id = a.job_id
WHERE strftime('%Y', a.datetime) = '2021'
GROUP BY 1,2
ORDER BY 1,2""")
#print(cur.fetchall())

cur.execute("""with hirings AS (
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
HAVING SUM(hired) > (SELECT AVG(hired) FROM hirings WHERE year_hired = '2021')
ORDER BY SUM(hired) desc""")
#print(cur.fetchall())

# Fetch all results from the query
results = cur.fetchall()

# Define the CSV file path
csv_file_path = 'output3.csv'

# Open a CSV file for writing
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Optionally write the header (column names) based on your query
    column_names = [description[0] for description in cur.description]
    writer.writerow(column_names)  # Writing header row
    
    # Write the data rows
    writer.writerows(results)

conn.close()
