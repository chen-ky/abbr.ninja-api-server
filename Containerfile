FROM docker.io/slatedocs/slate:latest AS docs

RUN apt-get update && apt-get install -y git
RUN gem update --system && bundle install

RUN git clone https://github.com/chen-ky/abbr.ninja-api-doc.git && ln -s 'abbr.ninja-api-doc/source' ./source

RUN bundle exec middleman build


FROM docker.io/library/python:alpine AS production

RUN apk update \
    && apk upgrade

RUN apk add \
    cargo \
    gcc \
    libc-dev \
    libffi-dev \
    mariadb-connector-c-dev

RUN adduser -H -D web

COPY --chown=web:web src/requirements.txt /srv/uri_shortener/src/requirements.txt

RUN pip install -r /srv/uri_shortener/src/requirements.txt

RUN apk del \
    cargo \
    gcc \
    libc-dev \
    libffi-dev

RUN chmod 0550 -R /srv/uri_shortener/

COPY --chown=web:web config.toml /etc/uri_shortener/config.toml
COPY --chown=web:web src /srv/uri_shortener/src/.
COPY --from=docs --chown=web:web /srv/slate/build /srv/uri_shortener/doc/build/.

USER web

EXPOSE 8081

WORKDIR "/srv/uri_shortener/src/"
CMD ["gunicorn", "main:main()", "-b 0.0.0.0:8081"]
