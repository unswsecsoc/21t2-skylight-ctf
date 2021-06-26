#!/bin/bash
app="secret-base-vuln"
docker build -t ${app} .
#TODO can we remove -v
docker run -d -p 9996:9996 --name=${app} -v $PWD:/app ${app}
