# C3D3 FastAPI
No dependencies.

---

C3D3 FastAPI backend helps to automate C3D3 Data Vault management.

# Configuration

First of all to configure FastAPI backend correctly need to do next steps:

- Clone current repository:
```
git clone https://github.com/e183b796621afbf902067460/c3d3-fastapi.git
```

- Get into the project folder:
```
cd c3d3-fastapi/src/microservices
```

- Set environment variables in [.env](https://github.com/e183b796621afbf902067460/c3d3-fastapi/blob/master/src/microservices/.env).

# Docker

- Run docker compose (`sudo`):
```
docker-compose up -d --build
```

- Check C3 and D3 container's ID and copy them:
```
docker ps
```

- Create AuthDB, C3Vault and D3Vault instances:
```
docker exec -it <CONTAINER ID> python3 app/orm/scripts/create.py
```

- Create default admin user in auth container:
```
docker exec -it <CONTAINER ID> python3 app/__init__.py
```

# Endpoints

- `/api/v1/auth/login`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/auth/login?self=self'
data = {"username": "default", "password": "default"}
header = {'accept': 'application/json', 'Content-Type': 'application/json'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/c3/new_account`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/c3/new_account?self=self'
data = {"label_name": "default", "label_api_key": "default", "label_api_secret": "default"}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/c3/new_account_balances`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/c3/new_account_balances?self=self'
data = {"exchange_name": "default", "instrument_name": "default", "label_name": "default"}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

# Exit
- To stop all running containers:
```
docker stop $(docker ps -a -q)
```
- And remove it all:
```
docker rm $(docker ps -a -q)
```
