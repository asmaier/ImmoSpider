#!/usr/bin/env bash
docker build -t immospider .
docker run -d --name immospider --env-file ./config immospider
# docker logs immospider
# docker cp df134a4abcc8:/app/apartments.csv docker_apartments.csv
