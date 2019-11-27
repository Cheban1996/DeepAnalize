FROM python:2-slim

RUN apt-get update && apt-get install

RUN pip install --no-cache-dir six>=1.7.3

RUN pip install --no-cache-dir wad

CMD ["wad", "-h"]