#!/bin/bash
app="new-office-vuln"
docker build -t ${app} .
#TODO can we remove -v
docker run -d -p 9997:9997 --name=${app} -v $PWD:/app ${app}
