FROM python:2.7.14-alpine3.6

RUN apk add --no-cache git bash grep

WORKDIR /wd

RUN git clone https://github.com/natrix-fork/Breacher .

RUN pip install --no-cache-dir requests

ENTRYPOINT ["python", "./breacher.py"]

CMD ["--help"]
