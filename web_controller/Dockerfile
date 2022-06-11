FROM python:3.9-alpine

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5000

RUN chmod +x job_posting.py
CMD ["python", "job_posting.py"]