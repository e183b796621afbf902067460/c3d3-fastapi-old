# DeFi FastAPI
Depends on: [defi-head-core](https://github.com/e183b796621afbf902067460/defi-head-core).

---

DeFi FastAPI backend helps to automate DeFi ETL management.

# Local Configuration

First of all to configure FastAPI backend correctly need to do next steps:

- Clone current repository:
```
git clone https://github.com/e183b796621afbf902067460/defi-fastapi.git
```

- Get into the project folder:
```
cd defi-fastapi/
```

- Set CORS in [settings.py](https://github.com/e183b796621afbf902067460/defi-fastapi/blob/master/src/cfg/settings.py) to allow [frontend](https://github.com/e183b796621afbf902067460/defi-react), for local setup:
```python
BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
       "http://localhost:3000"
       ]
```

- Set credentials in [engine.py](https://github.com/e183b796621afbf902067460/defi-fastapi/blob/master/src/orm/cfg/engine.py), for local setup:
```python
DB_ADDRESS = os.getenv('POSTGRES_HOST', '')
DB_USER = os.getenv('POSTGRES_USER', '')
DB_PASSWORD = quote_plus(os.getenv('POSTGRES_PASSWORD', ''))
DB_NAME = os.getenv('POSTGRES_DB', '')
```

- Create a virtual environment:
```
python3 -m venv venv
```

- Activate venv:
```
source venv/bin/activate
```

- Install requirements:
```
pip3 install -r requirements.txt
```

- Fill database with fixtures:
```
pytest tests/_fixtures/conftest.py
```

- Run FastAPI server using `uvicorn`:
```
uvicorn src.app:app --reload
```

`Result will be at` [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

# Docker
- Set the __ENV__ variables in `docker-compose.yaml`:
  
  - PostgreSQL environment variables in [backend](https://github.com/e183b796621afbf902067460/defi-fastapi/blob/master/docker-compose.yaml#L6) and [orm](https://github.com/e183b796621afbf902067460/defi-fastapi/blob/master/docker-compose.yaml#L29) services, by default:
  ```
  POSTGRES_HOST: orm
  POSTGRES_USER: defi_management
  POSTGRES_PASSWORD: defi_management
  POSTGRES_DB: defi_management
  ```
  - Server environment variables in [backend](https://github.com/e183b796621afbf902067460/defi-fastapi/blob/master/docker-compose.yaml#L6) service, by default:
  ```
  SERVER_HOST: 0.0.0.0
  SERVER_PORT: 8000
  ```
  - Set CORS in [settings.py](https://github.com/e183b796621afbf902067460/defi-fastapi/blob/master/src/cfg/settings.py), by default:
  ```python
  BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:3000'
        ]
  ```

- Run docker compose (`sudo`):
```
docker-compose up -d
```

`Result will be at` [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

# Exit
- To stop all running containers:
```
docker stop $(docker ps -a -q)
```
- And remove it all:
```
docker rm $(docker ps -a -q)
```
