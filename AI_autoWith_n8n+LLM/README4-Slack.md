# Slack Integration

## Test n8n Webhook

```bash
curl -X POST "http://localhost:5778/webhook/d707d430-f73a-4378-a6da-b7427c704cf9"  
 --data "text=what is overtime policy?"

    {"message":"Workflow was started"}
    
```

## Install ngrok

<https://dashboard.ngrok.com/get-started/your-authtoken>

```cmd
choco install ngrok
ngrok config add-authtoken $YOUR_TOKEN
ngrok http 5778

    Session Status                online
    Account                       samfire5200@gmail.com (Plan: Free)
    Update                        update available (version 3.28.0, Ctrl-U to update)
    Version                       3.22.1
    Region                        Japan (jp)
    Latency                       105ms
    Web Interface                 http://127.0.0.1:4040
    Forwarding                    https://e09bd5e2322e.ngrok-free.app -> http://localhost:5778
                                     
```

```bash
curl -X POST "https://e09bd5e2322e.ngrok-free.app/webhook/d707d430-f73a-4378-a6da-b7427c704cf9"   --data "text=what is overtime policy?"
```

## Setup of Slack API Bot

<https://api.slack.com/start/quickstart>

### **Slack App Setup Steps**

<https://api.slack.com/apps>

1. Creating an app => from scratch

   * App Name: `HR n8n Bot`
   * Workspace: `AI with n8n and LLMs` => Create App

2. OAuth & Permissions => Bot Token Scopes => Requesting scope permissions
   a. allow your app to post messages, add the `chat:write`
   b. allow your app to access public Slack channels, add the `channels:read`

3. Slash Command => Create New Command
   *Command: `/askHRn8n`
   *Request URL: `https://e09bd5e2322e.ngrok-free.app/webhook/d707d430-f73a-4378-a6da-b7427c704cf9`
   (replace with your actual n8n webhook URL)
   *Short Description: `Ask HR n9n Policy` => Save

4. App Home => Allow users to send Slash commands and messages from the messages tab (v)

5. Install and authorize our app

---

## n8n workflow

* 03 Qdrant w Slack

```chat
what is overtime policy?
```

### Docker compose

```cmd
cd n8n-workflows
// Edit .evn PUBLIC_BASE_URL=https://e09bd5e2322e.ngrok-free.app
docker compose down
docker compose up -d
```

```bash
curl -X POST "https://e09bd5e2322e.ngrok-free.app/webhook/d707d430-f73a-4378-a6da-b7427c704cf9"   --data "text=what is overtime policy?"
```

```note
ngrok URL will be revised each time.  Need to update all the above mentioned steps accordingly.
```
