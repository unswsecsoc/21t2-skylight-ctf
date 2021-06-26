#!/bin/bash
app="office-vuln"
docker build -t ${app} .

docker run -d -p 9998:9998 --name=${app} -v $PWD:/app ${app}
