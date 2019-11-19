# Wazo UI

Wazo-ui is an open source project for helping people to use easily the API of wazo-platform. This project is not up to date with all API in the engine, but you can do lot of features.

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
You need to add a config file in /etc/wazo-ui/conf.d/ for exemple engine.yml.

```
amid:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/amid
  verify_certificate: false
auth:
  host: <your_engine_ip_or_dns>
  port: 443
  timeout: 30
  prefix: /api/auth
  verify_certificate: false
call-logd:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/call-logd
  verify_certificate: false
confd:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/confd
  verify_certificate: false
dird:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/dird
  verify_certificate: false
plugind:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/plugind
  verify_certificate: false
provd:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/provd
  verify_certificate: false
webhookd:
  host: <your_engine_ip_or_dns>
  port: 443
  prefix: /api/webhookd
  verify_certificate: false
```

# Translations

To extract new translations:

    % python setup.py extract_messages

To create new translation catalog:

    % pybabel init -l <locale> --input-file=wazo_ui/translations/messages.pot --output-dir=wazo_ui/translations/


To update existing translations catalog:

    % python setup.py update_catalog

Edit file `wazo_ui/translations/<locale>/LC_MESSAGES/messages.po` and compile
using:

    % python setup.py compile_catalog

# Debugging bootstrap

To enable live-edit of bootstrap.min.css, you will need to add the following line at the end of
bootstrap.min.css file:

    /*# sourceMappingURL=bootstrap.min.css.map */
