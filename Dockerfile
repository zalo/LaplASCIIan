FROM debian:11-slim

RUN apt-get update && apt-get install python3 python3-pip python3-numpy python3-dev libgl1 ffmpeg libsm6 libxext6  -y

COPY ./api ./
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

#CMD ["/app/server"]