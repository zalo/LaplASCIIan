FROM debian:11-slim

RUN apt-get update && apt-get install libgl1 ffmpeg libsm6 libxext6  -y

COPY ./api ./
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

#CMD ["/app/server"]