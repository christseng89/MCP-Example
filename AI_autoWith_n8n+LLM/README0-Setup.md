# Setup environment for n8n workflows

## Install ngrok

<https://dashboard.ngrok.com/get-started/your-authtoken>

```cmd
choco install ngrok
ngrok config add-authtoken $YOUR_TOKEN
                      
```

## Install n8n to work with ngrok

```cmd
ngrok http 5778

    Session Status                online
    Account                       samfire5200@gmail.com (Plan: Free)
    Update                        update available (version 3.28.0, Ctrl-U to update)
    Version                       3.22.1
    Region                        Japan (jp)
    Latency                       105ms
    Web Interface                 http://127.0.0.1:4040
    Forwarding                    https://e09bd5e2322e.ngrok-free.app -> http://localhost:5778
               
cd n8n-workflows
// Edit .env file to set PUBLIC_BASE_URL=https://e09bd5e2322e.ngrok-free.app

docker-compose down
docker-compose up -d
docker compose exec n8n printenv | grep -E "CHART_API_KEY|JINA_API_KEY"
```

<http://localhost:5778/>

```cmd
docker exec -it n8n sh
    ls /home/node/.n8n/nodes/node_modules/ -l
    exit

docker logs n8n
```
