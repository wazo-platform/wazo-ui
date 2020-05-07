FROM python:3.7-buster

LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

# Configure environment
RUN true \
    && adduser --quiet --system --group --no-create-home --home /var/lib/wazo-ui wazo-ui \
    && mkdir -p /etc/wazo-ui/conf.d \
    && touch /var/log/wazo-ui.log \
    && chown wazo-ui /var/log/wazo-ui.log \
    && mkdir /run/wazo-ui/ \
    && chown wazo-ui /run/wazo-ui/ \
    && mkdir /var/lib/wazo-ui/ \
    && chown wazo-ui /var/lib/wazo-ui/ \
    && true

# Add certificates
ADD ./contribs/docker/certs /usr/share/xivo-certs
WORKDIR /usr/share/xivo-certs
RUN openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -nodes -config openssl.cfg -days 3650
RUN chown -R wazo-ui /usr/share/xivo-certs

# Install wazo-ui
ADD . /usr/src/wazo-ui
WORKDIR /usr/src/wazo-ui
RUN true \
    && pip install -r requirements.txt \
    && python setup.py install \
    && cp -av etc/wazo-ui /etc \
    && true

EXPOSE 9296

CMD ["wazo-ui", "-d"]
