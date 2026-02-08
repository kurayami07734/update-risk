## UpdateRisk Server

### Get started

#### Using docker and docker compose

1. Populate .env
2. Move to server directory and run using docker compose

```bash
docker compose up --build
```

#### Running locally (using uv)

1. Install uv
2. Move to server directory and install deps

```bash
uv sync
```

3. Run via fastapi CLI

```bash
fastapi dev src/main.py --port 8000
```