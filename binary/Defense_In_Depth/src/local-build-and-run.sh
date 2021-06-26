#!/bin/bash
app="skylight-vuln"
docker build -t ${app} .
#TODO can we remove -v
docker run -d -p 9999:9999 --name=${app} -v $PWD:/app ${app}
