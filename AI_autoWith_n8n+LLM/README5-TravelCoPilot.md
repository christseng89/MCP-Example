# Travel CoPilot - n8n Cloud

## Use case

SAM 是一位经常旅行的人，他希望能够更方便地与当地人交流、看懂外国餐馆的菜单，并理解道路标志。 ✅

## 旅行助手功能

### 无缝语音到语音翻译

* 用 55 种支持的语言之一交流，实时见证机器人将你的话语翻译成另一种语言，全程通过语音完成。

### 视觉翻译魔法

* 捕捉包含文字的图像，机器人会自动识别并翻译这些文字成所需的语言，并立即在你眼前显示。

---

## Telegram Bot Setup

<https://web.telegram.org/>

Telegram Bot: /BotFather -> /newbot => travelercopilot => travelercopilotChrisT_bot

```note
Done! Congratulations on your new bot. You will find it at t.me/travelercopilotChrisT_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxx
Keep your token secure and store it safely, it can be used by anyone to control your bot.

```

n8n => This **token** is required to connect to the Telegram Bot API.
click **t.me/travelercopilotChrisT_bot** to start the bot.

## n8n Workflow

*04 Travel CoPolit via Telegram (n8n)

## Work with Local Docker Compose

```bash
ngrok http 5778
```

Copy the `https://xxxxx.ngrok-free.app` URL.

### Tell n8n its external URL

Update your compose (or env) so n8n generates webhooks with that HTTPS base:

```yaml
environment:
  - N8N_EDITOR_BASE_URL=https://xxxxx.ngrok-free.app
  - WEBHOOK_URL=https://xxxxx.ngrok-free.app
```

Then restart n8n and follow the instructions of **Telegram Bot Setup**
