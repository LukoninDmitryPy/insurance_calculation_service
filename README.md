# Insurance Calculation Service

This service calculates insurance costs based on cargo type and declared value using configurable tariffs.

## Features
- REST API using FastAPI
- PostgreSQL database with SQLAlchemy ORM
- Kafka logging for actions
- Docker and Docker Compose deployment
- CRUD operations for tariffs
- Insurance cost calculation

## Setup and Deployment

1. Clone the repository:
```bash
git clone https://github.com/LukoninDmitryPy/insurance_calculation_service.git
```
3. Define variables
    Set params in alembic.ini(db::64), docker-compose.yaml(db::23-25), config.py
    ```bash
    cp src/config.py_template src/config.py
    ```
2. Start the services with Docker Compose:
   ```bash
   docker compose up --build -d
   ```
3. Init alembic
   ```bash
   docker exec -it web alembic revision --autogenerate -m "Name_of_migration"
   docker exec -it web alembic upgrade head
   ```
   on first start:
   ```bash
   docker compose restart web
   ```

## Kafka logs:
    ```bash
    docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic insurance_logs --from-beginning
    ```

## Example API usage

### SwaggerAPI on:
```
127.0.0.1:8000/docs
```
