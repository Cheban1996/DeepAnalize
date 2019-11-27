docker run -it -p 8118:8118 -p 9050:9050 -d dperson/torproxy
docker pull eoranged/rq-dashboard
docker run -p 9181:9181 eoranged/rq-dashboard
rq worker audit
rq-dashboard -p 9991
