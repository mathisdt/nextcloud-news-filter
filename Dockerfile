FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir requests

COPY ./main.py .

CMD [ "python", "./main.py" ]
