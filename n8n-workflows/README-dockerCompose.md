# A minimal Docker Compose setup to run n8n on Windows Docker Desktop

## Reference

<https://docs.n8n.io/integrations/community-nodes/installation/>

## 1 Create a data folder

```cmd
mkdir C:\n8n\n8n-data
mkdir C:\n8n\local-files
```

## 2 Create docker-compose.yaml

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5778:5678"
    environment:
      - NODE_ENV=production
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - N8N_HOST=localhost
      - GENERIC_TIMEZONE=Europe/Berlin
      - TZ=Europe/Berlin
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
      - N8N_RUNNERS_ENABLED=true
      # Optional basic auth
      # - N8N_BASIC_AUTH_ACTIVE=true
      # - N8N_BASIC_AUTH_USER=youruser
      # - N8N_BASIC_AUTH_PASSWORD=yourpass
    volumes:
      # Persist data (Windows path on left)
      - C:/n8n/n8n-data:/home/node/.n8n
      # Optional shared files
      - C:/n8n/local-files:/files
```

## 3 Start with Docker Compose

```bash
docker compose up -d
```

## 4 View in browser

<http://localhost:5778>
