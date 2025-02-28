import requests
from db import connect_with_connector
import sqlalchemy
import os

# The URL of the API endpoint
url = 'http://127.0.0.1:8080/data'

# Your API token
api_token = 'JMCC99'

# Set the headers with the API token
headers = {
    'Authorization': f'Bearer {api_token}',
}

# Send the GET request with the headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse and use the response (e.g., as JSON)
    data = response.json()
    print(data)
else:
    print(f'Failed to retrieve data: {response.status_code}')


env_connection_sql = {
    'project_id': 'micro-progress-452300-g0',
    'region': 'us-central1',
    'instance': 'de-challenge',
    'db_user': 'desarrollo',
    'db_pass': 'S0p0rt3@$',
    'db_name': 'postgres'
}
"""
db = connect_with_connector(env_connection_sql)
with db.connect() as conn:
    stmt = sqlalchemy.text(
        "INSERT INTO departments (department) VALUES (:department)"
    )
    conn.execute(stmt, parameters={"department": "Gestion Humana"})
    conn.commit()

    result = conn.execute(sqlalchemy.text("SELECT * FROM departments")).fetchall()
    print(result)

    for row in result:
        print(row)
    conn.close()
"""

"""
url = 'http://127.0.0.1:5000/upload_csv'
directory_path = 'files'
files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

for file in files:
    file_path = os.path.join(directory_path, file)

    with open(file_path, 'rb') as f:
        files = {'file': (file, f, 'text/csv')}
        data = {'table': os.path.splitext(os.path.basename(file_path))[0]} 
        response = requests.post(url, files=files, data=data, headers=headers)
    
    if response.status_code == 200:
        print("File uploaded")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
    print('Response JSON:', response.json())
"""
"""
url = 'http://127.0.0.1:5000/batch_insert'

json_data = {
    "table": "employees",
    "rows": [
        {"id": 9998, "name": "John Doe", "datetime": "2022-09-27 18:00:00.000", "department_id": 1, "job_id": 2},
        {"id": 9999, "name": "Jane Smith", "datetime": "2025-02-22 13:32:00.000", "department_id": 1, "job_id": 3}
    ]
}
response = requests.post(url, json=json_data, headers=headers)
print('Status Code:', response.status_code)
#print(response.text)
print('Response JSON:', response.json())
"""

url2 = 'http://127.0.0.1:8080/employees_by_quarter'
url3 = 'http://127.0.0.1:8080/employees_hired'

response = requests.get(url2, headers=headers)
print('Status Code:', response.status_code)
#print(response.text)
print('Response JSON:', response.json())

response = requests.get(url3, headers=headers)
print('Status Code:', response.status_code)
#print(response.text)
print('Response JSON:', response.json())