# Sec 10K Nvidia

## n8n Templates

<https://n8n.io/creators/derekcheungsa/>

*AI Crew to Automate Fundamental Stock Analysis - Q&A Workflow

## Download Nvidia Sec 10K

<https://investor.nvidia.com/financial-info/sec-filings/default.aspx>

## n8n Workflow

*05.1 Nvidia Sec10K Stock Analysis - RAG **Activate**
*05.2 Nvidia Sec10K Stock Analysis - Analysis

```note
Use n8n in Docker, change the localhost:5778 to n8n:5678 for 'webhook_url_sec10k_data' in 'Settings' node.
Such as: http://n8n:5678/webhook/19f5499a-3083-...

```

```bash test 05.1 Nvidia Sec10K Stock Analysis - RAG
curl -X POST http://localhost:5778/webhook/19f5499a-3083-4783-93a0-e8ed76a9f742   -H "Content-Type: application/json"   -d '{"input":"Provide SWOT Analysis for NVDA from the SEC 10-K filing","company":"nvda"}'       
```

```cmd
node n8n_subflow1.js
```

## 功能規格書：NVIDIA SEC 10-K 研究報告自動化（n8n）05.2 Nvidia Sec10K Stock Analysis - Analysis

### 1. 目的與價值

將「高階研究員 → 研究員分工 → 主編潤稿 → 發佈」的研究工作流自動化：

* 以 **SEC 10-K** 為唯一事實來源（可輔以維基摘要），產出**面向投資人**的完整公司研究報告。
* 自動上傳報告成品（純文字檔）到 **Google Drive**。

### 2. 範圍

* 公司範例：`nvda`（可改）
* 產出：1 份**經主編潤稿**的最終報告（純文字 .txt）上傳至「My Drive / root」
* 研究結構：由 \*\*高階研究員（AI）**規劃段落數、字數與研究提示，交由**研究員（AI）**撰寫各節內容，再由**主編（AI）\*\*統稿潤稿。

### 3. 先決條件

* n8n 可用，且已設定：

  * **OpenAI** 憑證（節點使用 `gpt-4o`）
  * **Google Drive OAuth2** 憑證
* 本地/外部 **SEC 10-K Webhook API** 可存取（POST）。預設 URL：
  `http://localhost:5778/webhook/19f5499a-3083-4783-93a0-e8ed76a9f742`（可改）&#x20;

### 4. 輸入/輸出

#### 4.1 輸入參數（Settings 節點）

* `company`: 預設 `"nvda"`
* `sections`: 預設 `5`（報告分段數）
* `words`: 預設 `2000`（報告總字數）
* `webhook_url_sec10k_data`: 供 SEC 10-K 查詢的 Webhook URL

#### 4.2 輸出成品

* 檔名：`nvidia_10kReport2025.txt`（可改）
* 位置：Google Drive 根目錄 `/`（可改）
* 內容：經統稿潤稿的完整報告純文字。

### 5. 主要角色（邏輯）

* **高階研究員（Plan work for team）**：產出標題/副標、導言/結論、圖像提示與各節「寫作提示」。
* **研究員（Do detailed research）**：依各節提示撰寫對應正文（以 SEC 10-K 為準；必要時輔以維基）。
* **主編（Polish report）**：以投資人語氣統稿潤筆，不遺漏研究員重點。
* **發佈員（Convert to File → Google Drive）**：輸出並上傳成品。

### 6. 節點規格（逐點）

> 下列以 n8n 節點名稱為主，括號內為節點類型。
> 省略之 Sticky Note 僅做說明用途，無執行邏輯。

1. **When clicking "Test workflow"**（Manual Trigger）

   * 手動啟動工作流。

2. **Settings**（Set）

   * 設定：`sections=5`、`words=2000`、`company="nvda"`、`webhook_url_sec10k_data=<URL>`
   * 產出設定物件供後續節點存取。

3. **SEC10 Tool / SEC10 Tool1**（LangChain Tool: Code）

   * 功能：將查詢問題 POST 到 `webhook_url_sec10k_data`，回傳 SEC 10-K 段落資訊。
   * 請求範例：`{ "input": "<question>", "company": "<company>" }`
   * 錯誤時回傳 `"error"` 並交由上游/下游處理。

4. **Wikipedia / Wikipedia1**（LangChain Tool: Wikipedia）

   * 輔助查閱背景（非主要事實來源）。

5. **Plan work for team**（OpenAI）

   * 模型：`gpt-4o`
   * 輸入：`company`、`words`、`sections`、工具（SEC10 Tool / Wikipedia）
   * 輸出（JSON）欄位：`title`、`subtitle`、`introduction`、`conclusions`、`imagePrompt`、`sections[]`（每節含 `title`、`prompt`）
   * 要求：全部內容以**最新 SEC 10-K**為據，邏輯連貫、避免重複。

6. **Delegate work**（Split Out）

   * 將 `message.content.sections[]` 拆分為多筆 item，供多次平行呼叫研究員節點。

7. **Do detailed research**（OpenAI）

   * 模型：`gpt-4o`；工具：SEC10 Tool1、Wikipedia1
   * 每個 item 依 `title` 與 `prompt` 產出對應正文段落（不含導言/結論/小標，約 `((words-120)/sections)` 字）。
   * 嚴格要求：以 SEC 10-K 為據；與前後節內容銜接、不重覆。

8. **Combine all sections from researchers**（Merge：mergeByPosition）

   * 將各節研究員結果按原順序合併。

9. **Draft report**（Code）

   * 功能：組稿。
   * 結構：

     * 前置加入 `introduction`
     * 依序將每節標題（加粗）與正文串接
     * 收尾加入 **Conclusions** 與 `conclusions` 文字
   * 輸出：`article`（完整草稿）。

10. **Polish report**（OpenAI）

    * 模型：`gpt-4o`
    * 任務：以投資人/專業口吻「意譯潤稿」，不可刪漏研究重點。
    * 輸出：最終報告正文（message.content）。

11. **Convert to File**（Convert to File → toText）

    * 將 `message.content` 轉為純文字檔 Buffer。

12. **Google Drive**（Google Drive）

    * 目標：`My Drive` / `root`
    * 檔名：`nvidia_10kReport2025.txt`
    * 行為：上傳前一節產生之文字檔。

### 7. 資料流程（高層級）

Manual Trigger → Settings → Plan work → Split（sections） → 多次 Do research → Merge → Draft → Polish → Convert→ GDrive 上傳。

### 8. 錯誤處理與回復策略

* **SEC10 Tool 回傳 `"error"`**：

  * 在 Do detailed research/Plan work 中加入判斷與重試（建議 3 次退避）。
  * 若持續失敗，於該節插入佔位文本（註記需人工補齊）並在最後報告附「缺頁附註」。
* **OpenAI Token/Quota 失效**：

  * 於三個 AI 節點加上錯誤輸出路徑（Error branch），統一寫入 n8n Execution Log 並觸發通知（可加 Slack/Email 節點）。
* **Google Drive 上傳失敗**：

  * 啟用重試，若仍失敗，將文字檔改存本地（n8n 節點臨時檔）並回報連結/路徑。

### 9. 安全與合規

* **唯一事實來源**：以 SEC 10-K 為準，Wikipedia 僅輔助背景。
* **憑證保護**：OpenAI、Google OAuth2 存於 n8n Credentials；禁用在節點內硬編碼金鑰。
* **Webhook 安全**：建議於 API Gateway 設 Header 驗證／IP 白名單／速率限制。

### 10. 參數化與在地化

* 可於 **Settings** 直接改：`company`、`sections`、`words`、`webhook_url_sec10k_data`。
* 檔名與上傳目錄可於 **Google Drive** 節點調整。

### 11. 非功能性需求

* **效能**：`sections` 不宜過多（>10）以避免 OpenAI token 超限與執行逾時。
* **可用性**：每節點增加最少限度的錯誤分支，並在失敗時保留中間產物（半成品報告）。

### 12. 驗收測試（建議案例）

1. **基本流程**：`company=nvda`、`sections=5`、`words=2000` 能正常產出並上傳 txt 至 Drive。
2. **Webhook 失效**：SEC10 Tool 收到 500/逾時 → 研究節插入佔位並出現缺頁附註。
3. **OpenAI 超限**：Polish 報 429 → 重試後成功；若仍失敗，輸出 Draft 版成品並註記。
4. **Drive 權限不足**：上傳失敗 → 本地保存備份並記錄錯誤。

### 13. 擴充建議

* **版本控管**：將 `article` 與最終稿同步上傳第二份至 Drive（附時間戳），或送往 Git（Docs Repo）。
* **格式輸出**：在 Convert 之前新增 Markdown→DOCX/PDF 轉換（透過 pandoc 或自製微服務）。
* **多公司批次**：外層迴圈遍歷公司代碼陣列，並動態命名輸出檔。
* **引用清單**：在 Draft report 追加「資料來源附錄」區塊（SEC 檔案連結與條目）。

---

### 附錄 A：主要欄位/資料結構

* **Plan work for team（輸出 JSON）**

  * `title`, `subtitle`, `introduction` (\~60詞), `conclusions` (\~60詞), `imagePrompt`, `sections[]`（`title`, `prompt`）
* **Draft report（輸出）**

  * `article`：導言 + 各節（**粗體節題** + 內文） + **Conclusions** 收尾。

---
