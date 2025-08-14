# Model Context Protocol (MCP)

---

## 🧾 Model Context Protocol (MCP) 概要

* **來源與發展**

  * 由 Anthropic 推出（Claude 的開發公司），2024/11/25 發布。
  * 初期反應平平，但後來迅速爆紅，目前已有超過 **15,000 個 MCP 伺服器**，成為 LLM 生態系的重要標準。

* **核心概念**

  * **MCP 就像 LLM 的 USB-C 標準**：提供統一介面連接各種工具（API）、資源（圖片、文字等）、Prompt 模板。
  * 具有 **網路效應**：愈多人使用，價值愈高。
  * 可跨 LLM 使用（ChatGPT、Claude…），不用重複開發。

* **為何需要 MCP**

  * LLM 本身只能處理文字生成、翻譯、總結、寫程式等基本任務。
  * 進階功能需透過「Function Calling」呼叫**外部工具**（API、Python、Web Search 等）。
  * 傳統 API 與 LLM 整合繁瑣，缺乏標準化。

* **MCP 的運作方式**

  1. **Host（例如：Claude Desktop、Cursor、Windsurf）**

     * ***內建 MCP Client***。
  2. **MCP Server**（抽象層）

     * 封裝 API、資源、Prompt。
     * 自動轉換 LLM 的指令為正確 API 調用。
  3. **工具/資源整合**

     * 一個 MCP Server 可同時連接***多個*** APIs、資料庫、Prompt Template。
     * 支援自我探索（list 功能），可自動列出支援的功能。

* **MCP 的優勢**

  * 標準化：所有 MCP 伺服器的介面一致，減少 API 整合成本。
  * 動態自我發現：LLM 可自動知道 MCP Server 支援哪些功能。
  * API 更新自動管理：**API 改版時，MCP Server 更新**即可，LLM 不需改動。
  * 可重複使用：相同 MCP Server 可跨不同 LLM Host 使用。

* **實際應用**

  * 將 LLM 轉變為具備強大工具鏈的 AI Agent（能查詢資料庫、使用 API、存取資源、套用 Prompt 模板）。
  * 範例：

    * 用 MCP Server 連接 GitHub、向量資料庫、WhatsApp、雲端工具等，讓 LLM 無縫使用。

---

✅ **總結**
MCP 是一個專為 LLM 設計的標準化協定，像「USB-C for LLM」，統一了工具、API、資源、Prompt 的接入方式，減少整合複雜度並具備網路效應。隨著愈來愈多開發者採用，它正在成為 AI 開發的核心基礎設施。

---

## 📝 Prompt 🎯 主要概念

1. **兩種類型的 Prompt**

   * **使用者提示 (User Prompt)**：使用者在應用程式中輸入的內容，例如在 ChatGPT、Claude、Flowise、Cursor 中直接輸入的文字。
   * **系統提示 (System Prompt)**：由開發者設定，每次 API 呼叫都會自動附加，為模型提供額外的上下文。

📝 Prompt 簡單對比：

| 項目       | System Prompt | User Prompt |
| -------- | ------------- | ----------- |
| 定義 AI 角色 | ✅             | ❌           |
| 設定長期行為   | ✅             | ❌           |
| 設定工具/MCP | ✅             | ❌           |
| 動態變數     | ✅             | ❌           |
| 即時查詢問題   | ❌             | ✅           |
| 臨時任務     | ❌             | ✅           |

---

### ✍ Prompt 工程基本原則

* **清晰且具體**：例如不要只寫「幫我做簡報」，而是「幫我製作 10 頁的 Q2 銷售簡報，包含 Q2 銷售績效、暢銷產品與 Q3 銷售目標」。
* **提供範例**：給出範例郵件或內容有助於模型理解。
* **鼓勵推理**：透過上下文引導模型更準確地完成任務。

---

### 🛠 系統提示 (System Prompt) 建議

* **最佳系統提示通常是「沒有系統提示」**，因為：

  * 系統提示會增加 API Token 消耗，變慢並增加成本。
  * LLM 本身已經有大型內建的系統提示，比你自訂的更強大。
* 只有在應用程式行為不正確時，才逐步補充系統提示。
* 系統提示結構可包含：

  1. **角色 (Role)**：AI 扮演的身份
  2. **目標 (Goal)**：要達成的任務
  3. **工具 (Tools/MCP)**：可使用的工具或 MCP server
  4. **規則 (Rules)**：行為規範
  5. **風格 (Style)**：語氣、格式（Markdown）、長度
  6. **範例 (Examples)**：簡短示例
  7. **變數 (Variables)**：例如當前日期時間、使用者名稱

---

### ⚡ 系統提示實務技巧

* 先從 **沒有系統提示** 開始，確認功能正常。
* 若出現錯誤，再針對問題逐步補充指令（例如加上日期時間或特定 MCP server 呼叫條件）。
* 可用 Flowise、Cursor、OpenAI Playground 自動產生初稿，然後再精簡不必要的部分。

---

## 🔑 關鍵觀念

* LLM 供應商（如 Anthropic Claude 4）的內建系統提示非常龐大（數百行），包含大量規則與範例，比自訂提示更強大。
* 系統提示會隨 API 呼叫重複傳送，增加延遲與成本。
* 只有在必要時才新增系統提示，並採取漸進式調整。

---

## 🛠 需要安裝的軟體

1. **Node.js** – 執行 NP 指令與大部分 MCP 伺服器
2. **NVM** – 管理 Node.js 版本
3. **Cloud Desktop** – 作為 MCP 伺服器的主要宿主環境
4. **VSCode** – 編輯 Cloud Desktop 設定檔
5. **MCP Installer** – 簡化 MCP 伺服器安裝流程
6. **Python** – 執行需要 Python 的 MCP 伺服器
7. **UV (Python 套件管理器)** – 管理 Python 套件
8. **Pyenv** – 管理 Python 版本

```cmd install pyenv-win
choco install pyenv-win
cd .pyenv
git checkout master
git pull

pyenv install --list

```

```cmd switch python version
pyenv install 3.12.10-arm
pyenv global 3.12.10-arm
pyenv local 3.12.10-arm
pyenv versions
pyenv which python
pyenv which pip
pyenv which uv

where python
python --version

```

---

## 🔐 MCP Server 主要安全風險

### 1. **未驗證來源的伺服器**

* **風險**：從不明網站下載或安裝 MCP 伺服器，可能包含惡意程式碼。
* **後果**：可能被植入惡意腳本，導致資料外洩或系統損壞。
* **防範**：僅使用官方 MCP 伺服器，或來自可信開發者的開源專案。

---

### 2. **工具中毒（Tool Poisoning）**

* **風險**：MCP 伺服器可能被惡意修改，將指令重導至危險操作（例如刪除本地檔案）。
* **後果**：損壞開發環境、刪除重要資料、安裝惡意軟體。
* **防範**：

  * 使用沙箱或虛擬環境測試伺服器。
  * 僅**授權最小**必要的檔案系統或 API 存取權限。

---

### 3. **過度授權**

* **風險**：給予 MCP 伺服器**過多**權限（如完整檔案系統存取）。
* **後果**：被惡意伺服器**刪除**或竄改檔案。
* **防範**：

  * 使用細粒度權限管理。
  * 僅開放必要目錄或 API 權限。

---

### 4. **伺服器棄置（Deprecation Risk）**

* **風險**：伺服器開發者**停止維護**，導致安全漏洞未修補。
* **後果**：持續使用舊版伺服器，**暴露在已知漏洞下**。
* **防範**：

  * 定期檢查伺服器更新。
  * 使用 MCP Installer 或版本管理工具更新至受支援版本。

---

### 5. **API Key 外洩**

* **風險**：某些 MCP 伺服器（例如 Zapier MCP）需使用 API Key。
* **後果**：API Key 被竊取後，可能導致**服務濫用**。
* **防範**：

  * 使用環境變數儲存金鑰。
  * 禁止將金鑰硬編碼進 MCP 設定檔。
  * 採用 API Key 旋轉機制。

---

### 6. **惡意攻擊（MacBreak Balls 攻擊）**

* **風險**：攻擊者透過惡意 MCP 伺服器執行**破壞性動作**，例如刪除或加密檔案。
* **後果**：本地系統資料**毀損**。
* **防範**：

  * 僅從官方 MCP 資料庫安裝伺服器。
  * 先在測試環境驗證，再部署到主要工作環境。

---

## ✅ 最佳安全實踐

* 只使用**官方**或**可信**來源的 MCP 伺服器。
* 啟用**最小化權限**（Principle of Least Privilege）。
* 定期**更新** MCP 伺服器與相關工具。
* 在本地**沙箱**環境先測試伺服器。
* 定期**審核**並移除不再使用的伺服器。
* 若使用 API Key，使用**安全存放**方式（如 `.env`）。
* 監控**伺服器的活動記錄**，及早發現異常行為。

---

## MCP Official Documentation

### MCP SDKs

* <https://modelcontextprotocol.io/docs/sdk>
* <https://modelcontextprotocol.io/quickstart/server>
  <https://modelcontextprotocol.io/examples>

### MCP Servers

* <https://modelcontextprotocol.io/quickstart/server>
* <https://modelcontextprotocol.io/examples>

### MCP Clients

* <https://modelcontextprotocol.io/quickstart/client>
  <https://modelcontextprotocol.io/clients>

### Tutorials

* <https://modelcontextprotocol.io/tutorials/building-mcp-with-llms>
* <https://modelcontextprotocol.io/quickstart/user#windows>

## **Claude 桌面應用程式（Claude Desktop）**，🧩 啟用 **開發者模式（Developer Mode）** 的步驟

1. 打開 **Claude Desktop 應用程式**（有橙色小狐狸圖示版本，確保非網頁或深色版本）
2. 點擊視窗左上角的 **漢堡選單（☰）**（Top‑Left Hamburger Menu） ([Reddit][1])
3. 從該選單選擇 **Help → Enable Developer Mode**，將其啟用 ([Anthropic][2])
4. 啟用後，於漢堡選單中會出現 **Developer** 項目
5. 點擊 **Settings → Developer → Edit Config** 可編輯設定檔案 ([Medium][3])

---

## Awesome MCP Servers

*<https://github.com/punkpeye/awesome-mcp-servers>
*<https://glama.ai/mcp/servers>

## Awesome MCP Clients

*<https://github.com/punkpeye/awesome-mcp-clients/>
*<https://glama.ai/mcp/clients>

## Zapier MCP Server

*<https://zapier.com/>

Zapier 的作用很簡單但很強大——它是一個 **線上自動化平台**，可以幫你把不同的應用程式和服務連接起來，讓它們之間自動傳輸資料、執行任務，而不需要自己寫程式。

它的主要用途與功能包括：

### 1️⃣ 連接不同應用（整合 API）

* 例如：Gmail、Google Sheets、Slack、Trello、Notion、Salesforce、HubSpot 等上千種服務。
* 即使兩個應用程式沒有直接的整合功能，Zapier 也能透過它的中間層 API 連接起來。

---

### 2️⃣ 自動化工作流程（Zaps）

* 你可以設定一個「觸發條件」（Trigger）+ 一個或多個「動作」（Action）。
* 例子：

  * **Trigger（觸發條件）**：有人填寫 Google 表單
  * **Action（動作）**：Zapier 自動把資料新增到 Airtable，並且發一則 Slack 通知
* 這樣你就不用手動去做這些動作，系統會自動完成。

---

### 3️⃣ 節省時間與人力

* 把重複、機械化的任務交給 Zapier，例如：

  * 新的訂單自動寫入 Google Sheets
  * 客服信件自動分派到指定的團隊
  * 社群文章自動同步到多個平台

---

### 4️⃣ 無需程式知識

* 不用寫代碼就能做跨平台整合，對非工程人員也非常友好。
* 介面是拖拉式設定，邏輯類似「IF 發生了這個，THEN 做那個」。

---

💡 **簡單比喻**：Zapier 就像一個**自動化郵差**，根據你的規則，幫你把不同應用之間的資訊傳來傳去，還能同時寄到多個地方。

---

## n8n

### Install n8n

```cmd
nvm use 18.15.0
npm install -g n8n

nvm use 20.19.4
npm update -g n8n

n8n user-management:reset --email admin@example.com --password "ChangeMe123" --firstName Admin --lastName User
n8n
```

### **1️⃣ n8n 是什麼？**

**n8n**（讀作 “n-eight-n”）是一個 **開源、自託管 或 雲端的自動化工具**，主要功能是：

* **工作流程自動化（Automation）**：用節點（Node）將不同應用、API、資料處理步驟連接起來。
* **資料處理能力強**：內建 JavaScript 代碼節點，可在流程中直接處理資料、調用 API。
* **部署靈活**：可以本地部署（On-Prem）、私有雲、或使用官方雲服務（n8n.cloud）。
* **開源協議**：根據 **公平代碼授權（Fair Code License）**，個人與內部商用免費，但 SaaS 再販售需要付費授權。

---

**n8n** 和 **Zapier** 都是工作流程自動化（workflow automation）平台，但理念、靈活度、部署方式和成本結構都不同。

### **2️⃣ n8n vs Zapier 對比表**

| 特性         | **n8n**                             | **Zapier**              |
| ---------- | ----------------------------------- | ----------------------- |
| **定位**     | 開源、自託管或雲端的自動化平台                     | 商業雲端自動化平台               |
| **部署方式**   | 本地部署（Docker、VM、K8s）、私有雲、官方雲         | 只能使用 Zapier 雲端          |
| **價格**     | 自託管免費（除非作為 SaaS 出售）；n8n.cloud 按用量計費 | 月費制（免費版限制多），根據任務數量與功能分級 |
| **應用整合數量** | 內建 \~350+ 節點，可接任何 API（自定義節點）        | 內建 6,000+ 應用整合（不需程式）    |
| **資料處理能力** | 高度可編程（支援 JavaScript、變量、條件邏輯）        | 低程式需求（大多數情況不能寫代碼）       |
| **學習曲線**   | 偏高（需理解工作流程邏輯與 API 基礎）               | 較低（點選設定即可）              |
| **安全性**    | 資料可留在內部網路（自託管模式）                    | 所有資料經過 Zapier 雲端        |
| **擴展性**    | 可開發自定義節點、支援複雜流程與分支                  | 擴展有限，以官方支援應用為主          |
| **適用對象**   | **技術團隊**、需數據隱私、需複雜邏輯的企業                 | 中小企業、行銷團隊、無程式背景的用戶      |

---

## **3️⃣ 簡單理解**

* **Zapier** = **上手快、應用多、封閉平台、付費 SaaS**
  適合**不想管理伺服器、需要大量應用整合**的人。
* **n8n** = **靈活可編程、可自託管、開源**
  適合**技術團隊、對資料隱私敏感、需要複雜流程控制**的企業。

---

💡 **簡單比喻**

* **Zapier**：像租用一個裝修好的辦公室（方便、交租金即可，但規則是房東定的）
* **n8n**：像擁有自己的辦公樓（自由裝修、自己管理、需要懂技術，但完全掌控 ***）

---

## Workflow **n8n（或類似自動化平台）建立工作流的基礎概念**

1. **工作流的基本結構**

   * 必須包含 **觸發器 (Trigger)** 和 **動作 (Action)**
   * 觸發器：啟動流程的條件（例：聊天訊息、郵件、Google Drive 檔案上傳、Webhook、定時事件等）
   * 動作：觸發後執行的任務（例：寄送郵件、呼叫 API、觸發 AI Agent、存入資料庫等）

2. **觸發器種類很多** (Event triggers)

   * 內建支援多種應用（Google、AWS、AirTable、Facebook、GitHub 等）
   * 支援 Webhook、AMQP Server、由其他工作流觸發、定時觸發等

3. **動作與資料處理**

   * 動作節點可以是 AI Agent，也可以連接外部 API 或工具
   * 節點間以 **JSON 格式** 傳遞資料，可手動映射（Mapping）
   * 可加入工具（Tools）、記憶（Memory）等輔助功能

4. **MCP 的應用**

   * 在同一個工作流中可以同時建立 **MCP Server** 和 **MCP Client**
   * MCP Client 可由 AI Agent 呼叫並與 MCP Server 溝通
   * MCP Server 可以連接任意其他客戶端

5. **核心原則**

   * **先理解基礎，再做複雜工作流**
   * 觸發器和動作可以自由組合
   * MCP 能讓不同工作流與外部系統靈活互通

---

### n8n Triggers Types

* **Trigger manually**
   Runs the flow on clicking a button in n8n. Good for getting started quickly

* **On app event**
   Runs the flow when something happens in an app like Telegram, Notion or Airtable

* **On a schedule**
   Runs the flow every day, hour, or custom interval

* **On webhook call**
   Runs the flow on receiving an HTTP request

* **On form submission**
   Generate web forms in n8n and pass their responses to the workflow

* **When executed by another workflow**
   Runs the flow when called by the Execute Workflow node from a different workflow

* **On chat message**
   Runs the flow when a user sends a chat message. For use with AI nodes

* **When running evaluation**
   Run a dataset through your workflow to test performance

* **Other ways…**
   Runs the flow on workflow errors, file changes, etc.

---

### Camunda + n8n Workflow Example

```flow
Applicant -> Camunda(Start)
Camunda(Service Task "OCR") --> n8n(Webhook /ocr)
n8n --> External APIs (OCR/AI)
n8n --> Camunda(POST /message feesCalculated + variables)
Camunda(Message Catch) -> continues to Approval
```

### Test OpenAI API

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

```

### Connect to Google Sheet step-by-step

1. **Create your Google Cloud project**

   * Console → Create project (e.g., `mcp-BuildAgents`).

2. **Enable APIs**

   * APIs & Services → Enable: **Google Sheets API** and **Google Drive API**.

3. **Configure OAuth consent screen**

   * User type: **External**.
   * App name: e.g., `mcp-BuildAgents`.
   * Add your email under **Test users**.
   * Scopes: add only what you need (e.g. `…/auth/spreadsheets`, `…/auth/drive.file`).
   * Save (no need to submit for verification if you stay in testing and only test users use it).

4. **Create OAuth 2.0 Client (Web application)**

   * Authorized redirect URIs (match your n8n URL):

     ```text
     http://localhost:5678/rest/oauth2-credential/callback
     ```

   * (If n8n runs on another host/port, change accordingly.)

5. **Fill n8n credentials** (`Google Sheets OAuth2 API`)

   * Paste the **Client ID** and **Client Secret** you just created.
   * Click **Sign in with Google** and pick the same account you added as a Test user.

6. **If you still see 403 access\_denied**

   * Make sure the Google account you select is in **Test users**.
   * Remove/replace any old credential in n8n that still references **mcp-BuildAgents**.
   * Check the redirect URI matches exactly (scheme/host/port/path).
   * If behind a proxy, set `N8N_HOST` and `N8N_EDITOR_BASE_URL` so n8n builds the same callback URL you whitelisted.

> TL;DR: Don’t use the unverified “mcp-BuildAgents” OAuth app. Create your own OAuth client, add yourself as a Test user, and use that Client ID/Secret in n8n.
