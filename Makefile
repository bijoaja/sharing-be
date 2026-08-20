.PHONY: up down migrate create-table stamp up-dev down-dev migrate-dev create-table-dev stamp-dev

# Load .env variables biar bisa dipake di command
include .env
export

# --- prod ---
up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose exec article alembic upgrade head

create-table:
	docker compose exec -T db mysql -u"$${MYSQL_USER}" -p"$${MYSQL_PASSWORD}" article < article/scripts/create_posts_table.sql

stamp:
	docker compose exec article alembic stamp head

# --- dev ---
up-dev:
	docker compose -f docker-compose.dev.yml up -d

down-dev:
	docker compose -f docker-compose.dev.yml down

migrate-dev:
	docker compose -f docker-compose.dev.yml exec article alembic upgrade head

create-table-dev:
	docker compose -f docker-compose.dev.yml exec -T db mysql -u"$${MYSQL_USER}" -p"$${MYSQL_PASSWORD}" article < article/scripts/create_posts_table.sql

stamp-dev:
	docker compose -f docker-compose.dev.yml exec article alembic stamp head
