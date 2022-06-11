FROM python:3.9-alpine

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

RUN chmod +x work_queue.py
CMD ["python", "work_queue.py"]