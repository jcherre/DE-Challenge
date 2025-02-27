import requests

url = 'http://127.0.0.1:5000/batch_insert'
url2 = 'http://127.0.0.1:5000/employees_by_quarter'
url3 = 'http://127.0.0.1:5000/employees_hired'

json_data = {
    "table": "employees",
    "rows": [
        {"name": "John Doe", "datetime": "2022-09-27 18:00:00.000", "department_id": 1, "job_id": 2},
        {"name": "Jane Smith", "datetime": "2025-02-22 13:32:00.000", "department_id": 1, "job_id": 3}
    ]
}
#response = requests.post(url, json=json_data)
response = requests.get(url3)
print('Status Code:', response.status_code)
#print(response.text)
print('Response JSON:', response.json())
