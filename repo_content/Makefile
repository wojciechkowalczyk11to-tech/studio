.PHONY: dev test lint format build deploy clean logs shell db-migrate kb-build kb-upload

dev:
	docker compose up -d

test:
	docker compose exec backend pytest

lint:
	ruff check . && mypy .

format:
	ruff format .

build:
	docker compose build

deploy:
	./scripts/deploy.sh

clean:
	docker compose down -v

logs:
	docker compose logs -f

shell:
	docker compose exec backend bash

db-migrate:
	docker compose exec backend alembic upgrade head

kb-build:
	python knowledge-base/scripts/harvest_github.py

kb-upload:
	python knowledge-base/scripts/upload_to_vertex.py
