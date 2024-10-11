run:  ##@Run app
	docker compose up

build:  ##@Build app and database
	docker compose -f docker-compose.yml build

env: ##@Generate env file
	cp .env.example .env

