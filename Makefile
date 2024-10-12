build:
	docker build -t my_fastapi_app .

run:
	docker run -d -p 8000:8000 my_fastapi_app

install:
	pip install -r requirements.txt

local-run:
	uvicorn main:app --host 0.0.0.0 --port 8000