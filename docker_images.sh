#!/bin/bash

docker build -t deep_analize/wad:1.0 audits/wad/docker/
docker build -t deep_analize/pompem:1.0 audits/wad_pompem/docker/
docker build -t deep_analize/show_exploit:1.0 audits/show_exploit/docker/
docker build -t deep_analize/brutex:1.0 audits/brutex/docker/
docker build -t deep_analize/breacher:1.0 audits/breacher/docker/
docker build -t deep_analize/blazy:1.0 audits/blazy/docker/
docker build -t deep_analize/wapiti:1.0 audits/wapiti/docker/
