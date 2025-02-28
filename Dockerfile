FROM python:3.10.4-buster

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV FLASK_ENV=production

CMD ["gunicorn", "-b", "0.0.0.0:8080", "cloud.app:create_app()"]
