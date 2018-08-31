docker build -t immospider .
docker run -t --env-file ./config immospider
# docker cp df134a4abcc8:/app/apartments.csv docker_apartments.csv
