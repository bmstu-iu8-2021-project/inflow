

compose:
	sudo chown helga:helga -R .temp
	docker-compose up --build

clean:
	docker-compose down
