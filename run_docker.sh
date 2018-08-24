docker build -t immospider .
docker run -t -e URL=https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/-/2,50-/60,00-/EURO--1000,00 immospider
# docker cp df134a4abcc8:/app/apartments.csv docker_apartments.csv
