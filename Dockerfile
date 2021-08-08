FROM docker.io/library/python:alpine

RUN apk update \
    && apk upgrade

RUN apk add \
    gcc \
    libc-dev \
    mariadb-connector-c-dev

RUN pip install \
    bleach \
    falcon \
    gunicorn \
    mariadb \
    pycryptodome \
    toml

RUN apk del \
    gcc \
    libc-dev

RUN adduser -H -D web

COPY config.toml /etc/uri_shortener/config.toml
COPY --chown=web:web src /srv/uri_shortener/src/.
COPY --chown=web:web doc/build /srv/uri_shortener/doc/build/.

RUN chmod 0550 -R /srv/uri_shortener/

USER web

EXPOSE 8081

WORKDIR "/srv/uri_shortener/src/"
CMD ["gunicorn", "main:main()", "-b 0.0.0.0:8081"]
