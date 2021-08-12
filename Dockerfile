FROM docker.io/library/python:alpine

RUN apk update \
    && apk upgrade

RUN apk add \
    gcc \
    libc-dev \
    mariadb-connector-c-dev

RUN adduser -H -D web

RUN pip install -r src/requirements.txt

COPY config.toml /etc/uri_shortener/config.toml
COPY --chown=web:web src /srv/uri_shortener/src/.
COPY --chown=web:web doc/build /srv/uri_shortener/doc/build/.

RUN apk del \
    gcc \
    libc-dev

RUN chmod 0550 -R /srv/uri_shortener/

USER web

EXPOSE 8081

WORKDIR "/srv/uri_shortener/src/"
CMD ["gunicorn", "main:main()", "-b 0.0.0.0:8081"]
