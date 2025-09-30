FROM python:3.11-slim-bookworm AS compile-image
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

RUN python -m venv /opt/venv
# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /usr/src/wazo-ui/requirements.txt
WORKDIR /usr/src/wazo-ui
RUN pip install -r requirements.txt

COPY . /usr/src/wazo-ui
RUN python setup.py install

FROM python:3.11-slim-bookworm AS build-image
COPY --from=compile-image /opt/venv /opt/venv

COPY ./etc/wazo-ui /etc/wazo-ui
RUN true \
    && adduser --quiet --system --group --home /var/lib/wazo-ui wazo-ui \
    && mkdir -p /etc/wazo-ui/conf.d \
    && install -o wazo-ui -g wazo-ui /dev/null /var/log/wazo-ui.log

EXPOSE 9296

# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"
CMD ["wazo-ui", "-d"]
