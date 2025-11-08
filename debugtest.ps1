.\.venv\Scripts\activate

flask --app . init-db
flask --app . add-user 202320020 1234
flask --app . run --debug
