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
