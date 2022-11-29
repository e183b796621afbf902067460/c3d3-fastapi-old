#!/bin/bash

export PYTHONPATH=funds/:/home/user/repositories/defi-microservice-funds/
/home/user/repositories/defi-microservice-funds/venv/bin/uvicorn funds.main:app --host 127.0.0.1 --port 8080 --reload