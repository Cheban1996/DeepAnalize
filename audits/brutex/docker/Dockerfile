FROM debian:9.3-slim

WORKDIR /wd

RUN echo "deb http://http.kali.org/kali kali-rolling main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb-src http://http.kali.org/kali kali-rolling main contrib non-free" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends --allow-unauthenticated \
        ca-certificates \
        git \
        nmap \
        hydra \
        dnsenum

RUN git clone https://github.com/natrix-fork/BruteX .

RUN chmod +x ./brutex

ENTRYPOINT ["./brutex"]
