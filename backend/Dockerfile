FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:7000" ] 