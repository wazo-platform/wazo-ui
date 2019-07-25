FROM python:3.5-stretch

LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

ADD . /usr/src/wazo-ui
WORKDIR /usr/src/wazo-ui
RUN true \
    && set -x \
    && pip install -r requirements.txt \
    && python setup.py install \
    && adduser --quiet --system --group --no-create-home --home /var/lib/wazo-ui wazo-ui \
    && cp -av etc/wazo-ui /etc \
    && mkdir -p /etc/wazo-ui/conf.d \
    && touch /var/log/wazo-ui.log \
    && chown wazo-ui /var/log/wazo-ui.log \
    && mkdir /var/run/wazo-ui/ \
    && chown wazo-ui /var/run/wazo-ui/ \
    && mkdir /var/lib/wazo-ui/ \
    && chown wazo-ui /var/lib/wazo-ui/ \
    && true

ADD ./contribs/docker/certs /etc/wazo-ui/https
WORKDIR /etc/wazo-ui/https
RUN openssl req -x509 -newkey rsa:4096 -keyout private-key.pem -out public-certificate.pem -nodes -config openssl.cfg -days 3650
WORKDIR /usr/src/wazo-ui

EXPOSE 9296

CMD ["wazo-ui", "-fd"]
