# Flowise DockerQuick path (SQLite, 1 container)

## 1) Prereqs

* **Docker Desktop for Windows** installed & running. ([Docker Documentation][1])

## 2) Make folders (for persistent data)

Open **PowerShell** and create a working directory:

```cmd
md flowise\data
cd flowise
```

## 3) Create `.env`

Create `.env` with these contents (tweak as needed):

```dotenv
# App
PORT=3100
DEBUG=false

# Database (SQLite by default)
DATABASE_TYPE=sqlite
DATABASE_PATH=/root/.flowise

# Credentials encryption key (persist this!)
SECRETKEY_STORAGE_TYPE=local
SECRETKEY_PATH=/root/.flowise
FLOWISE_SECRETKEY_OVERWRITE=replace-with-a-long-random-string

# Storage & logs
BLOB_STORAGE_PATH=/root/.flowise/storage
LOG_PATH=/root/.flowise/logs
```

(Flowise uses these env vars for port, DB, storage, and encryption key.) ([FlowiseAI][2])

## 4) Create `docker-compose.yml`

Save this as `C:\flowise\docker-compose.yml`:

```yaml
version: "3.9"
services:
  flowise:
    image: flowiseai/flowise:latest
    container_name: flowise
    ports:
      - "3100:3100"
    env_file: .env
    volumes:
      - "C:/flowise/data:/root/.flowise"
    restart: unless-stopped
```

## 5) Start it

From `C:\flowise`:

```powershell
docker compose up -d
```

Open [http://localhost:3100](http://localhost:3100) in your browser. (These are the official Docker quick-start steps, adapted for Windows paths.) ([FlowiseAI][3])

> **Tip (port busy?)**: change both `PORT` in `.env` and the left side of the mapping to e.g. `3001:3001`, then `docker compose up -d`. ([FlowiseAI][2])

---

# Optional: Postgres + pgvector (recommended for bigger RAG sets)

If you’d rather not use SQLite, add a Postgres service (with pgvector) and point Flowise at it.

## 1) Extend `.env`

Replace DB section with:

```dotenv
DATABASE_TYPE=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_USER=flowise
DATABASE_PASSWORD=ChangeMe
DATABASE_NAME=flowise
```

(These are the supported DB env vars.) ([FlowiseAI][2])

## 2) Extend `docker-compose.yml`

```yaml
version: "3.9"
services:
  db:
    image: pgvector/pgvector:pg16
    container_name: flowise-db
    environment:
      - POSTGRES_DB=flowise
      - POSTGRES_USER=flowise
      - POSTGRES_PASSWORD=ChangeMe
    ports:
      - "5432:5432"
    volumes:
      - "C:/flowise/postgres:/var/lib/postgresql/data"
    restart: unless-stopped

  flowise:
    image: flowiseai/flowise:latest
    container_name: flowise
    depends_on:
      - db
    ports:
      - "3100:3100"
    env_file: .env
    volumes:
      - "C:/flowise/data:/root/.flowise"
    restart: unless-stopped
```

Bring it up:

```powershell
docker compose up -d
```

(Flowise documents Postgres/pgvector usage and shows a compose example.) ([FlowiseAI][4])

---

# Optional: High-throughput “queue” mode (Redis + worker)

For heavy loads, Flowise can run a **queue** with a web server + background worker + Redis:

* Add to `.env`:

```dotenv
MODE=queue
QUEUE_NAME=flowise-queue
REDIS_URL=redis://redis:6379
WORKER_PORT=5566
```

* Add Redis and a second Flowise worker service in compose (pattern per docs). ([FlowiseAI][5])

---

# Daily use

* **Stop / start**

  ```powershell
  docker compose stop
  docker compose start
  ```
* **Upgrade Flowise** (keeps your data because it’s on `C:\flowise\data`)

  ```powershell
  docker compose pull
  docker compose up -d
  ```

  (You can also build/run straight from the repo, but compose with the prebuilt image is the easiest.) ([FlowiseAI][3])

---

# Windows-specific notes

* **Volume path syntax**: in `docker-compose.yml` use `C:/...` forward-slash style on Windows (as shown above).
* **Persistence**: your SQLite DB, encryption key, uploaded files, and logs all live under `/root/.flowise` in the container → mapped to `C:\flowise\data`. Keeping the **`FLOWISE_SECRETKEY_OVERWRITE`** set prevents “credentials could not be decrypted” surprises after upgrades. ([FlowiseAI][2], [GitHub][6])
* **Firewall/LAN access**: if you need to reach Flowise from other machines, allow inbound on TCP **3100** in Windows Defender Firewall.
* **Port 3100 collision**: change the `PORT` and the port mapping if something else already uses 3100. ([FlowiseAI][2])

---

If you tell me whether you prefer **SQLite** (simplest) or **Postgres/pgvector**, I can drop in the exact compose file you can paste and run.

[1]: https://docs.docker.com/desktop/setup/install/windows-install/?utm_source=chatgpt.com "Install Docker Desktop on Windows"
[2]: https://docs.flowiseai.com/configuration/environment-variables "Environment Variables | FlowiseAI"
[3]: https://docs.flowiseai.com/getting-started "Get Started | FlowiseAI"
[4]: https://docs.flowiseai.com/integrations/langchain/vector-stores/postgres?utm_source=chatgpt.com "Postgres | FlowiseAI"
[5]: https://docs.flowiseai.com/configuration/running-flowise-using-queue?utm_source=chatgpt.com "Running Flowise using Queue | FlowiseAI"
[6]: https://github.com/FlowiseAI/Flowise/issues/896?utm_source=chatgpt.com "[BUG] Credentials could not be decrypted · Issue #896"
