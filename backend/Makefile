APPLICATION_NAME = app
TEST = poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG

lint:  ##@Code Check code with pylint
	poetry run python -m pylint $(APPLICATION_NAME) tests

format:  ##@Code Reformat code with isort and black
	poetry run python -m isort $(APPLICATION_NAME) tests
	poetry run python -m black $(APPLICATION_NAME) tests

db:  ##@Database Create database with docker-compose
	docker-compose -f docker-compose.yml up -d --remove-orphans

test:  ##@Testing Test application with pytest
	make db && $(TEST)

test-cov:  ##@Testing Test application with pytest and create coverage report
	make db && $(TEST) --cov=$(APPLICATION_NAME) --cov-report html --cov-fail-under=70

