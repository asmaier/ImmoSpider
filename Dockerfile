FROM kennethreitz/pipenv

COPY . /app

COPY yacrontab.yaml /etc/yacron.d/yacrontab.yaml

# ENTRYPOINT ["/yacron/bin/yacron"]

CMD yacron -c /etc/yacron.d/yacrontab.yaml
# CMD scrapy crawl immoscout -o apartments.csv -a url=$URL  -L INFO
