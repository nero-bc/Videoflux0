FROM itsherchoice/videoflux2:latest

COPY . /app
WORKDIR /app
RUN chmod 777 /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD sh start.sh
