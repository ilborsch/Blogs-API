# Docker commands to build

docker-compose run app alembic revision --autogenerate -m "New Migration"

docker compose run app alembic upgrade head

alembic init alembic 

docker-compose build

docker-compose up

