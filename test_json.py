import requests

url = 'http://127.0.0.1:5000/batch_insert'

json_data = {
    "table": "employees",
    "rows": [
        {"name": "John Doe", "datetime": "2022-09-27 18:00:00.000", "department_id": 1, "job_id": 2},
        {"name": "Jane Smith", "datetime": "2025-02-22 13:32:00.000", "department_id": 1, "job_id": 3}
    ]
}
response = requests.post(url, json=json_data)
print('Status Code:', response.status_code)
print('Response JSON:', response.json())
