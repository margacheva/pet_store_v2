# pet_store

- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- docker run --name yana_db -e POSTGRES_USER=yana -e POSTGRES_PASSWORD=yana -p 44444:5432 -d postgres
- cd app
- export FLASK_APP=app
- flask run