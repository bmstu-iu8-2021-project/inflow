

compose:
	docker-compose up --build

clean:
	docker-compose down
	docker volume rm inflow_postgres_data

dev:
	FLASK_APP=src/server.py FLASK_ENV=development flask run --port 3000
