FROM kennethreitz/pipenv

COPY . /app

CMD scrapy crawl immoscout -o apartments.csv -a url=$URL  -L INFO
