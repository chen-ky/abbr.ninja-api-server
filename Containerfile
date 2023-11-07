FROM ruby:2.6-slim as docs

WORKDIR /srv

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        nodejs

RUN git clone https://github.com/chen-ky/abbr.ninja-api-doc.git slate

WORKDIR /srv/slate

RUN gem install bundler \
    && bundle install

RUN apt-get remove -y build-essential git \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x /srv/slate/slate.sh
RUN /srv/slate/slate.sh build


FROM docker.io/library/python:alpine AS production

RUN apk update --no-cache \
    && apk upgrade --no-cache

RUN apk add --no-cache \
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
