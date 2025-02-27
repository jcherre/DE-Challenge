import requests
import os

url = 'http://127.0.0.1:5000/upload_csv'
directory_path = 'files'
files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

for file in files:
    file_path = os.path.join(directory_path, file)

    with open(file_path, 'rb') as f:
        files = {'file': (file, f, 'text/csv')}
        data = {'table': os.path.splitext(os.path.basename(file_path))[0]} 
        response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        print("File uploaded")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
    print('Response JSON:', response.json())