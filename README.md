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

- Set the __SERVER_HOST__, __SERVER_PORT__ and __BACKEND_CORS_ORIGINS__ variables in [settings.py](https://github.com/e183b796621afbf902067460/defi-fastapi/blob/master/src/cfg/settings.py), for local setup:
```python
SERVER_HOST: str = '127.0.0.1'
SERVER_PORT: int = 8080
BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000"
    ]
```

- Set credentials in [engine.py](https://github.com/e183b796621afbf902067460/defi-fastapi/blob/master/src/orm/cfg/engine.py), for local setup:
```python
DB_ADDRESS = os.getenv('DB_ADDRESS', 'localhost')
DB_USER = os.getenv('DB_USER', 'username')
DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', 'password'))
DB_NAME = os.getenv('DB_NAME', 'defi')
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

- Init database schema:
```
pytest tests/init.py
```

- Run FastAPI server using `uvicorn`:
```
uvicorn src.app:app --reload
```
