FROM ubuntu:18.04

# -- Install Pipenv:
RUN apt update && apt install python3-pip git -y && pip3 install pipenv

# -- install berkley-db
RUN apt install -y libdb-dev 

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system

# install app

COPY . /app
COPY yacrontab.yaml /etc/yacron.d/yacrontab.yaml

# ENTRYPOINT ["/yacron/bin/yacron"]

CMD yacron -c /etc/yacron.d/yacrontab.yaml
# CMD scrapy crawl immoscout -o apartments.csv -a url=$URL  -L INFO
