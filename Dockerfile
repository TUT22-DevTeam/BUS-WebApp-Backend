FROM python:3.9-slim

WORKDIR /app
COPY /app/ ./
COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD ["uvicorn", "bus_db:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]