FROM python:3.9-slim

WORKDIR /app

COPY consumer1.py /app/consumer1.py

RUN pip install --no-cache-dir azure-eventhub azure-eventhub-checkpointstoreblob-aio

CMD ["python", "consumer1.py"]
