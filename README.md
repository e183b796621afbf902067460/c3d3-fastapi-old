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

# Exit
- To stop all running containers:
```
docker stop $(docker ps -a -q)
```
- And remove it all:
```
docker rm $(docker ps -a -q)
```

# Alembic
- After any changes in DBs this command should be done in `/app/orm` path:
```
alembic revision --autogenerate
```
- And make migrations:
```
alembic upgrade head
```
