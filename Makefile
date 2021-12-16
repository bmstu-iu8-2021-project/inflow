

compose:
	docker-compose up --build

clean:
	docker volume rm inflow_postgres_data

dev:
	FLASK_APP=src/server.py FLASK_ENV=development flask run --port 3000

psql:
	docker exec -it inflow_pg_db psql -h 127.0.0.1 -U inflow-client -p 5432 -d inflow
