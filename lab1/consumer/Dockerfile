FROM python:3.9-slim

WORKDIR /app

COPY consumer1.py /app/consumer1.py

RUN pip install azure-eventhub azure-eventhub-checkpointstoreblob

CMD ["python", "consumer1.py"]
