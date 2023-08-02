Use python 3.11
Enter commands one by one before start coding


    python -m venv .venv
    .\.venv\Scripts\activate
    pip install -r requirements.txt
    pre-commit init
    alembic init migrations



To add new text to translate, enter

    pybabel extract -F .\babel.cfg -o .\locales\messages.pot .

To sync a new translation file, enter

    pybabel update -d locales -D messages -i locales/messages.pot
