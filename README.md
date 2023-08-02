Python 3.11


To add new text to translate, enter

    pybabel extract -F .\babel.cfg -o .\locales\messages.pot .

To sync a new translation file, enter

    pybabel update -d locales -D messages -i locales/messages.pot
