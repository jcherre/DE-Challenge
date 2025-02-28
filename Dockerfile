# Use an official Python runtime as a parent image
FROM python:3.10.4-buster

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]
