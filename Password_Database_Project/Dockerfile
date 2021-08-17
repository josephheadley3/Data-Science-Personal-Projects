FROM alpine
COPY . /app

FROM python:3

WORKDIR /usr/src/app

RUN python3 -m pip install tabulate

COPY . .

CMD [ "python", "./pwdb.py" ]
