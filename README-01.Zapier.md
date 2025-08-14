# **Zapier MCP Server 安裝與 Cloud Desktop 設定指南**，包含解決 OAuth 驗證限制的 workaround

## ⚡ 1. 前置需求

請先確保以下軟體已安裝：

1. **Node.js (v18+)**
2. **NVM**（可選，用於 Node.js 版本管理）
3. **Cloud Desktop**（MCP 執行環境）
4. **VSCode**（編輯設定檔）
5. **MCP Installer**
6. **Python + UV + Pyenv**（非必要，但建議安裝）

---

## 🔧 2. 安裝 Zapier MCP Server

### 方式 1：使用 MCP Installer（建議）

```bash
mcp install zapier
```

### 方式 2：手動安裝

```bash
npm install -g @modelcontext/zapier-mcp-server
```

---

## ⚙ 3. 設定 Cloud Desktop

1. 開啟 `~/.mcp/config.json`（或 Cloud Desktop 的設定檔）。
2. 加入以下內容：

```json
{
  "servers": {
    "zapier": {
      "command": "zapier-mcp-server",
      "args": [],
      "env": {
        "ZAPIER_API_KEY": "your-zapier-api-key",
        "ZAPIER_CLIENT_ID": "your-client-id",
        "ZAPIER_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

---

## 🔑 4. OAuth 驗證問題（Cloud Desktop workaround）

在 Cloud Desktop 環境下，Zapier 的 OAuth 流程無法彈出瀏覽器，需採用以下解法：

### 方法 A：本機授權後同步設定

1. 在本機終端機執行：

   ```bash
   zapier-mcp-server auth
   ```

   → 會彈出瀏覽器，完成 Zapier 帳號授權。
2. 授權成功後，將生成的憑證檔案（通常位於 `~/.mcp/zapier/credentials.json`）複製到 Cloud Desktop 同一路徑下。

---

### 方法 B：使用 API Key

* 登入 [Zapier 開發者平台](https://platform.zapier.com/)。
* 建立「Private App」，並取得 **API Key**。
* 在 `config.json` 內直接設定 `ZAPIER_API_KEY`，略過 OAuth。

---

## 🚀 5. 測試連線

安裝完成後，重新啟動 Cloud Desktop，並確認 Zapier MCP Server 是否啟動：

```bash
mcp list
```

應能看到：

```note
zapier-mcp-server    RUNNING
```

然後可用以下指令測試：

```bash
mcp exec zapier list-apps
```

→ 會列出支援的 7,000+ 應用程式。

---

## 🛡 6. 安全性建議

* 先使用官方 App 測試（如 Gmail、Google Sheets），避免使用第三方未審核 App。
* 定期更新 `zapier-mcp-server` 版本：

  ```bash
  npm update -g @modelcontext/zapier-mcp-server
  ```

* 控制 API Key 權限，避免給予過大範圍的存取權限。
* 若需多人使用，建議採用 **service account**，而非個人 OAuth。

---

## Zapier w n8n 運作方式

Zapier 可以用來**把多個 MCP Services 的入口集中起來**，再透過它生成一個統一的 Webhook URL，然後這個 URL 就能當作 **n8n 的一個 MCP Client Tool** 來用。

---

### 運作方式

1. **多個 MCP Services → Zapier**

   * 你在 Zapier 裡建立不同的 Trigger/Action（每個 Trigger 對應一個 MCP Service 的請求）。
   * Zapier 會把這些動作包裝成單一 API Webhook（或 Zapier 提供的任務入口）。

2. **Zapier → n8n**

   * 在 n8n 的 MCP Client 設定中，只要加一個 Tool，URL 指向 Zapier 的 Webhook URL。
   * 這樣 n8n 就等於透過這個「代理 URL」可以間接呼叫多個 MCP Services。

---

### 優點

* **集中管理**：不需要在 n8n 一一配置每個 MCP Service 的 endpoint。
* **多服務合併**：不同 MCP 的結果可以在 Zapier 內先處理，再回傳給 n8n。
* **快速擴展**：要新增 MCP Service 時，只改 Zapier 的 Flow，不用動 n8n。

---

### 缺點

* **多一層延遲**：資料經過 Zapier 轉發會比直接連接慢。
* **額外成本**：Zapier 有免費方案限制，高頻使用要付費。
* **資料流經第三方**：敏感資料要注意隱私與安全。

---

如果你要的重點是 **Cursor / ChatGPT MCP 客戶端可以一次存取多個不同的 MCP Services**，其實除了 Zapier，也可以用 **自建 supergateway** 或 **n8n 自身 workflow** 來做類似的 MCP Multiplex 功能，這樣就不會受限於 Zapier 的流量與安全性。
