APP_PATH = wilde

.PHONY: run
run:
	docker compose up db redis -d --build
	python -m $(APP_PATH)

.PHONY: up
up:
	docker compose up -d --build

.PHONY: generate
generate:
	docker compose up db redis -d --build
	alembic revision --m="$(NAME)" --autogenerate

.PHONY: upgrade
upgrade:
	docker compose up db redis -d --build
	alembic upgrade head

.PHONY: format
format:
	ruff format .

.PHONY: lint
lint:
	ruff check . --fix
	mypy $(APP_PATH) --install-types --enable-incomplete-feature=NewGenericSyntax

.PHONY: freeze
freeze:
	uv export --format requirements-txt > requirements.txt
