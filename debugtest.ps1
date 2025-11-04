.\.venv\Scripts\activate

flask --app . init-db
flask --app . add-user 202320020 09062004
flask --app . run --debug