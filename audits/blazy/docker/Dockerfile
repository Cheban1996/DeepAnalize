FROM python:2.7-alpine3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /wd

RUN apk add --no-cache git
RUN git clone https://github.com/natrix-fork/blazy-1 ./ && apk del git

# runtime dependencies
RUN apk add --no-cache libxml2 libxslt

# build dependencies
RUN apk add --no-cache --virtual .build-deps gcc python-dev build-base libxml2-dev libxslt-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

ENTRYPOINT ["python", "blazy.py"]
