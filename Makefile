

compose:
	sudo chown helga:helga -R .temp
	docker-compose up --build

clean:
	docker-compose down

dev:
	FLASK_APP=src/server.py FLASK_ENV=development flask run --port 3000
