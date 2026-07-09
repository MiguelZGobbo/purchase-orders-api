.PHONY: install install-dev run test lint format seed docker-up docker-down clean

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements/development.txt

run:
	flask run

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .

seed:
	python scripts/seed.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache test.db
