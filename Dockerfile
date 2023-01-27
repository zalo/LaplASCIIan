FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install libgl1 ffmpeg libsm6 libxext6  -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./api .

CMD [ "python3", "-m" , "index.py"]
