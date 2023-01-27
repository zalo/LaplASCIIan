FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
RUN export FLASK_APP=index

RUN apt-get update && apt-get install libgl1 ffmpeg libsm6 libxext6  -y

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./api .

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 index:app
