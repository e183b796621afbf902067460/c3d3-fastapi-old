# POST

## auth/
- `/api/v1/auth/login`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/auth/login?self=self'
data = {
  "username": "string",
  "password": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json'}

response = r.post(url=url, json=data, headers=header)
```

## c3/
- `/api/v1/c3/new_account`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/c3/new_account?self=self'
data = {
  "label_name": "string",
  "label_api_key": "string",
  "label_api_secret": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/c3/new_account_balances`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/c3/new_account_balances?self=self'
data = {
  "exchange_name": "string",
  "instrument_name": "string",
  "label_name": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/c3/new_account_limit_orders`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/c3/new_account_limit_orders?self=self'
data = {
  "exchange_name": "string",
  "instrument_name": "string",
  "label_name": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/c3/new_account_liquidations`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/c3/new_account_liquidations?self=self'
data = {
  "exchange_name": "string",
  "instrument_name": "string",
  "label_name": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/c3/new_whole_market_trades_history`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/c3/new_whole_market_trades_history?self=self'
data = {
  "exchange_name": "string",
  "instrument_name": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

## d3/

- `/api/v1/d3/new_chain`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/d3/new_chain?self=self'
data = {
  "network_name": "string",
  "native_chain_token": "string",
  "rpc_node": "string",
  "block_limit": 0,
  "network_uri": "string",
  "network_api_key": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/d3/new_bids_and_asks`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/d3/new_bids_and_asks?self=self'
data = {
  "pool_address": "string",
  "network_name": "string",
  "protocol_name": "string",
  "specification_name": "string",
  "is_reverse": true
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/d3/new_hedge_to_borrows`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/d3/new_hedge_to_borrows?self=self'
data = {
  "wallet_address": "string",
  "token_address": "string",
  "network_name": "string",
  "label_name": "string",
  "protocol_name": "string",
  "specification_name": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/d3/new_hedge_to_supplies`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/d3/new_hedge_to_supplies?self=self'
data = {
  "wallet_address": "string",
  "token_address": "string",
  "network_name": "string",
  "label_name": "string",
  "protocol_name": "string",
  "specification_name": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/d3/new_wallet_balances`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/d3/new_wallet_balances?self=self'
data = {
  "wallet_address": "string",
  "token_address": "string",
  "network_name": "string",
  "label_name": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': '<access_token>'}

response = r.post(url=url, json=data, headers=header)
```
