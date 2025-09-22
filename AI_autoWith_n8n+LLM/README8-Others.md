# n8n more workflows

## 06.1 PDF to Chat with AI Vision

<https://go.freightforwarding.dhl.com/glo/ocean-freight-market-update-gated>

*glo-dgf-ocean-market-update.pdf
*OFR_Market_Update_Sep25.pdf
*06.1 PDF to Chat with AI Vision

```chat
what is the purpose of this document
please summarize the main insights of the document
give me the details about freight rate
```

## 06.2 Multi-agent PDF to Ghost Blog

### Use cases

*📑 Medical Research -> 📘 Accessible Health Articles
*💰 Financial Reports -> 📊 Insightful Market Analysis
*🎓 Academic Papers -> 📄 Engaging Blog Posts

### Setup Ghost

ID: samfire5200
Password: t0nnn#Xxxxx

### Create a custom integration (where the keys are issued)

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

### n8n workflow for PDF to Ghost Blog

*06.2 Multi-agent PDF to Ghost Blog
*Gartner’s Top Strategic Predictions for 2024.pdf
*Gartner's-2025-top-tech-trends-ebook.pdf

## 06.3 AI Powered Web Scraping

<https://docs.google.com/spreadsheets/d/1VDbfi2PpeheD2ZlO6feX3RdMeSsm0XukQlNVW8uVcuo/edit?pli=1&gid=258629074#gid=258629074>

### Jina AI

<https://jina.ai/>
<https://r.jina.ai/http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html>

### n8n workflow for AI Powered Web Scraping

*06.3 AI Powered Web Scraping

## 06.4 Technical Analyst AI Agent

### Chart Image Generation

<https://chart-img.com/>
<https://doc.chart-img.com/#introduction>

```bash test
curl -X POST "https://api.chart-img.com/v2/tradingview/advanced-chart/storage" \
  -H "x-api-key: Your-Chart-Img-API-Key" \
  -H "content-type: application/json" \
  -d '{
    "symbol": "NASDAQ:BITS",
    "theme": "dark",
    "studies": [
      {"name": "Bollinger Bands"},
      {"name": "Volume"},
      {"name": "Relative Strength Index"}
    ]
  }' \
  -o bits-chart.json
```

### n8n workflow for Technical Analyst AI Agent

* 06.4 Technical Analyst for Stock AI Agent

```Chat
do technical analysis for BITS
do technical analysis for AAPL
do technical analysis for MSFT
```

## 06.5 Research AI Agent with Auto Citation

<https://www.perplexity.ai/account/details> # Cannot get API key

### n8n workflow

*06.5 Research AI Agent Team with Auto Citation

```chat
Best practice to scan maven projects by using open sources via CI/CD
Effective parenting methods
The best practices SCA open-source tools for Maven projects
```

## 06.6 From Data to Insights Faster

<https://nocodb.com/>
<https://app.nocodb.com/#/wyacm8xy/pzfyqtxn1mbhi4p/mq0qyzxouxjapt5>

```note
Import Data => Excel => US+Stock+Valuation+Data+Set.xlsx => Import Files => Import
Table ID: mq0qyzxouxjapt5
Host: https://app.nocodb.com
Workspace: samfire5200
```

```chat
what was the total debt for AAPL in 2023?
what was the total debt for GOOG in 2023?
what was the total debt for MSFT in 2023?
what was the total debt for AAPL in 2021, 2022, and 2023?
what was the total assets of AAPL in 2023?
```

### Install nocodb in Docker

```cmd
cd nocodb
docker-compose up -d
```

<http://localhost:8090/>

### n8n workflow for Data to Insights

*06.6 From Data to Insights Faster - Part I

## 06.6 From Data to Insights Faster - Part II Visualization

```chat
what was AAPL EPS 2019-2023?
what was GOOG EPS 2019-2023?
compare the two with visualization
include MSFT in the comparison
visualize the profit margins
what data would be useful to visualize with a radar chart?
what about a bubble chart?
```

### n8n workflow for Data to Insights Visualization

*06.6 From Data to Insights Faster - Part II Visualization

## 06.7 From Data to Insights Faster - Part III DeepSeek + Telegram

### **DeepSeek Cost Comparison**

*For input processing, **DeepSeek-V3 (\$0.27 /1M tokens)** is 9.3x cheaper than **GPT-4o (\$2.50 /1M tokens)**.
*For output processing, **DeepSeek-V3 (\$1.10 /1M tokens)** is 9.1x cheaper than **GPT-4o (\$10.00 /1M tokens)**.
*In conclusion, **DeepSeek-V3** is more cost-effective overall.

```Telegram chat
what was AAPL EPS 2019-2023?
what was GOOG EPS 2019-2023?
compare the two with visualization
include MSFT in the comparison
visualize the profit margins
what data would be useful to visualize with a radar chart?
what about a bubble chart?
```

### n8n workflow for Data to Insights DeepSeek + Telegram

*06.7 From Data to Insights Faster - Part III DeepSeek + Telegram

```note
Settings -> Table ID: mq0qyzxouxjapt5
```

## 06.8 Build Your AI News Research Team - 24/7 Newsletter Automation with Citations

### n8n workflow for AI News Research Team

*06.8 Build Your AI News Research Team
