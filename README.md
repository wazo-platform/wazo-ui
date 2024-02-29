# Wazo UI

Wazo-ui is an open source UI to help people easily interact with the wazo-platform APIs.
This project is not always up-to-date with the entire API engine, but you can still do a lot.

![Login screenshot](/contribs/screenshots/login.png?raw=true "Login")
![Main screenshot](/contribs/screenshots/main.png?raw=true "Main")

# How to install

In the wazo platform installed.

    apt install wazo-ui

With docker.

    docker build -t wazo-ui .
    docker run -p 9286:9286 -v my_config_directory:/etc/wazo-ui/conf.d wazo-ui

On a fresh debian buster installed.

Add the wazo-platform repository and

    apt install wazo-ui

From the source

    # in a virtualenv
    pip3 install -r requirements.txt
    python3 setup.py install


# How to configure to use the engine remotely

If you want to use the UI in another VM or in a container.
You need to add a config file in /etc/wazo-ui/conf.d/ for example engine.yml.

```
amid:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/amid
  https: true
  verify_certificate: false
auth:
  host: <your_engine_ip_or_dns>
  port: 443
  timeout: 30
  prefix: /api/auth
  https: true
  verify_certificate: false
call-logd:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/call-logd
  https: true
  verify_certificate: false
confd:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/confd
  https: true
  verify_certificate: false
dird:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/dird
  https: true
  verify_certificate: false
plugind:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/plugind
  https: true
  verify_certificate: false
provd:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/provd
  https: true
  verify_certificate: false
webhookd:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/webhookd
  https: true
  verify_certificate: false
websocketd:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/websocketd
  verify_certificate: false
```

# Translations

To extract new translations:

    % python3 setup.py extract_messages

To create new translation catalog:

    % pybabel init -l <locale> --input-file=wazo_ui/translations/messages.pot --output-dir=wazo_ui/translations/


To update existing translations catalog:

    % python3 setup.py update_catalog

Edit file `wazo_ui/translations/<locale>/LC_MESSAGES/messages.po` and compile
using:

    % python3 setup.py compile_catalog

# Transifex

To use with transifex. The configuration is set in .tx directory.

    tx pull -t -l \<lang\> (eg. fr)
    python3 setup.py compile_catalog
    wdk mount wazo-ui
    wdk restart wazo-ui

# Debugging bootstrap

To enable live-edit of bootstrap.min.css, you will need to add the following line at the end of
bootstrap.min.css file:

    /*# sourceMappingURL=bootstrap.min.css.map */
