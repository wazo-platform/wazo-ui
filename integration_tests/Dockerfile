FROM wazoplatform/wazo-ui

COPY . /usr/src/wazo-ui
WORKDIR /usr/src/wazo-ui

ENV PYTHONDONTWRITEBYTECODE='true'

RUN pybabel compile --directory=wazo_ui/translations
RUN python setup.py develop
