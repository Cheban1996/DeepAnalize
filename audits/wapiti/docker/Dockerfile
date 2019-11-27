FROM python:3.6-alpine3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /opt

ENV VERSION_WAPITI 3.0.0

RUN apk add --no-cache openssl libxml2 libxslt

RUN apk add --no-cache --virtual .build-deps libxml2-dev libxslt-dev python3-dev musl-dev gcc \
    && wget "http://downloads.sourceforge.net/project/wapiti/wapiti/wapiti-$VERSION_WAPITI/wapiti-$VERSION_WAPITI.tar.gz" \
    && tar xvzf wapiti-$VERSION_WAPITI.tar.gz \
    && rm -f wapiti-$VERSION_WAPITI.tar.gz \
    && cd wapiti-$VERSION_WAPITI \
    && python setup.py install \
    && ln -sf /opt/wapiti-$VERSION_WAPITI /opt/wapiti \
    && chmod 755 /opt/wapiti/bin/wapiti \
    && apk del .build-deps

WORKDIR /wd

RUN adduser -D -s /bin/sh user user && chown -R user /wd

USER user

ENV LANG en
ENV PATH /opt/wapiti/bin:$PATH
ENV HOME /wd

ENTRYPOINT ["wapiti"]
