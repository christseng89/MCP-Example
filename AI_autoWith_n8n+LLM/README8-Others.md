# n8n more workflows

## 06.1 PDF to Chat with AI Vision

*glo-dgf-ocean-market-update.pdf
*06.1 PDF to Chat with AI Vision

```note
what is the purpose of this document
please summarize the main insights of the document
give me the details about freight rate
```

## 06.2 Multi-agent PDF to Ghost Blog

### Use cases

*📑 Medical Research -> 📘 Accessible Health Articles
*💰 Financial Reports -> 📊 Insightful Market Analysis
*🎓 Academic Papers -> 📄 Engaging Blog Posts

## Setup Ghost

## Create a custom integration (where the keys are issued)

1. Log into your Ghost Admin panel as an **Owner** (owner-level access is required):
   `https://your-ghost-site.com/ghost/`
2. In the left menu, go to **Settings → Integrations**.
3. Click **“Add custom integration”** (or **“Add integration”** → **Custom integration**).
4. Give the integration a name (e.g., `My Admin Tool`) and save.
5. After creation you will see two keys shown for that integration:

   * **Content API Key** — read-only, for public content (use for front-end/read operations).
   * **Admin API Key** — admin-level key string (format: `id:secret`) used to call the Admin API.
6. **Copy the Admin API Key** (the UI shows it once). Store it securely (secrets store / environment variable).

> Note: If you don’t see the Integrations menu or cannot create custom integrations, verify you’re logged in as the site **Owner** and that your Ghost installation version supports integrations (almost all recent versions do). For Ghost(Pro) customers the process is the same via Admin UI.

---

### Ghost Content API

<https://docs.ghost.org/content-api>
<https://docs.ghost.org/admin-api/posts/creating-a-post>

#### Create a JWT token

```cmd
node n8n_ghost.js
   eyJhbGciOiJIUzI1NiI...
```

curl -X POST https://ai-automation-with-n8n.ghost.io/ghost/api/admin/posts/?source=html \
  -H "Authorization: Ghost <JWT_Token>" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [
        {
            "title": "My test post",
            "html": "<p>My post content. Work in progress...</p>",
            "status": "published"
        }
    ]
  }'

### n8n workflow

*06.2 Multi-agent PDF to Ghost Blog