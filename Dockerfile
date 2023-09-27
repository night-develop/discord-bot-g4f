FROM python:3.10

RUN mkdir -p /srv/discord-bot-g4f/
WORKDIR /srv/discord-bot-g4f/
COPY . /srv/discord-bot-g4f/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD python3 main.py