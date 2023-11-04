FROM python:3.9


ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y ffmpeg wget unzip p7zip-full curl busybox aria2

RUN mv /usr/bin/aria2c /usr/bin/bf
RUN mv /usr/bin/ffmpeg /usr/bin/zender

COPY . /app
WORKDIR /app
RUN chmod 777 /app

RUN wget https://rclone.org/install.sh
RUN chmod 777 ./install.sh
RUN bash install.sh
RUN mv /usr/bin/rclone /usr/bin/mcl

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PORT = 8000
EXPOSE 8000

CMD sh start.sh