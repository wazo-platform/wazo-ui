# Wazo UI

## Translations

To extract new translations:

    % python setup.py extract_messages

To create new translation catalog:

    % pybabel init -l <locale> --input-file=wazo_ui/translations/messages.pot --output-dir=wazo_ui/translations/


To update existing translations catalog:

    % python setup.py update_catalog

Edit file `wazo_ui/translations/<locale>/LC_MESSAGES/messages.po` and compile
using:

    % python setup.py compile_catalog


## Debugging bootstrap

To enable live-edit of bootstrap.min.css, you will need to add the following line at the end of
bootstrap.min.css file:

    /*# sourceMappingURL=bootstrap.min.css.map */
