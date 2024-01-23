FROM python:3.9-slim

WORKDIR /app

COPY producer1.py /app/producer1.py

RUN pip install azure-eventhub requests

CMD ["python", "producer1.py"]
