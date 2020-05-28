FROM python:3.7-slim-buster AS compile-image
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

RUN python -m venv /opt/venv
# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"

COPY . /usr/src/wazo-ui
WORKDIR /usr/src/wazo-ui
RUN pip install -r requirements.txt
RUN python setup.py install

FROM python:3.7-slim-buster AS build-image
COPY --from=compile-image /opt/venv /opt/venv

COPY ./etc/wazo-ui /etc/wazo-ui
COPY ./contribs/docker/certs /usr/share/xivo-certs
RUN true \
    && adduser --quiet --system --group --home /var/lib/wazo-ui wazo-ui \
    && mkdir -p /etc/wazo-ui/conf.d \
    && install -d -o wazo-ui -g wazo-ui /run/wazo-ui/ \
    && install -o wazo-ui -g wazo-ui /dev/null /var/log/wazo-ui.log \
    && openssl req -x509 -newkey rsa:4096 -keyout /usr/share/xivo-certs/server.key -out /usr/share/xivo-certs/server.crt -nodes -config /usr/share/xivo-certs/openssl.cfg -days 3650 \
    && chown wazo-ui:wazo-ui /usr/share/xivo-certs/*


EXPOSE 9296

# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"
CMD ["wazo-ui", "-d"]
