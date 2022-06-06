FROM python:3.9-alpine

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

ENV FLASK_APP=main
CMD ["flask", "run", "--host", "0.0.0.0"]