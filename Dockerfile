FROM python:latest

MAINTAINER Janith Perera

RUN apt-get update -y

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
