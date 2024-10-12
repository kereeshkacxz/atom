build:
	docker build -t my_fastapi_app .

run:
	docker run -d -p 8000:8000 my_fastapi_app
