FROM python:3.10.4-buster

WORKDIR /src
COPY . /src

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV FLASK_ENV=production

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:create_app()"]
