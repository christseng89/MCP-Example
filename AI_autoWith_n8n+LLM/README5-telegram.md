# 🚀 Telegram Bot + n8n + ngrok 全流程手冊

## 1. 建立或重用 Telegram Bot

1. 打開 **web.telegram.org**，搜尋並進入 **@BotFather**。
2. 建立新 bot：

   ```input
   /newbot
   ```

   * 輸入顯示名稱（如：`travelercopilot`）
   * 輸入帳號（必須以 `_bot` 結尾，如：`travelercopilotChrisT_bot`）
   * BotFather 會給你一個 **Token**，形如：

     ```note
     123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxx
     ```

3. 如果你要重用既有的 bot：

   * `/mybots` → 選擇你的 bot → **Bot Settings → API Token** → **Copy**
   * 若 Token 遺失或外洩 → `/revoke` 重置，BotFather 會發新 Token。

⚠️ **Token 要填到 n8n Telegram Credentials 裡**。

---

## 2. 清除舊 Webhook（保險做法）

避免舊 URL 還掛著，先清掉：

```bash
curl -s "https://api.telegram.org/bot8274628539:AAEACLFU41-PTCBaXnm0oeZZXvvQz2uT4UQ/deleteWebhook"
```

成功會回：

```json
{"ok":true,"result":true,"description":"Webhook was deleted"}
```

---

## 3. 開啟 ngrok 建立 HTTPS 隧道

1. 在本機執行：

   ```bash
   ngrok http 5778
   ```

   會顯示一個 HTTPS URL，例如：

   ```note
   https://xxxxx.ngrok-free.app → http://localhost:5778
   ```

2. 複製這個 `https://xxxxx.ngrok-free.app`。

---

## 4. 編輯 `.env` 檔案

在 `docker-compose.yaml` 同層目錄建立或更新 `.env`：

```dotenv
...
PUBLIC_BASE_URL=https://xxxxx.ngrok-free.app
...
```

---

## 5. 重啟 n8n 容器

```bash
docker compose up -d       # 第一次啟動
docker compose restart n8n # 之後若 .env URL 改動
```

---

## 6. 在 n8n 配置 Telegram

1. 打開 \*\*[http://localhost:5778\*\*。](http://localhost:5778**。)
2. 新增 **Telegram API Credentials**，填入 BotFather 給的 Token。
3. 在工作流中加上 **Telegram Trigger** 節點：

   * **Update Mode** = `Webhook`（正式）或 `Polling`（測試用）。
   * 選剛剛的憑證。
4. **執行一次工作流（Execute workflow）**，n8n 會用 `.env` 的 `WEBHOOK_URL` 向 Telegram 註冊 Webhook。

---

## 7. 測試 Bot

* 在 Telegram 聊天中輸入訊息給 `@travelercopilotChrisT_bot`。
* 確認 n8n workflow 被觸發。

---

## 📝 注意事項

* **ngrok 免費版**：每次重啟 ngrok URL 都會變 → 更新 `.env` → `docker compose restart n8n` → 在工作流 **Execute 一次**。
* **ngrok 付費版**：可綁固定子網域，省去頻繁修改。
* 正式環境建議走 **自家網域 + Nginx/Traefik + TLS**，Webhook 更穩定。
* 群組支援：若要讓 bot 接收所有群訊息，在 @BotFather 執行 `/setprivacy` → Disable。

---
