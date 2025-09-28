# n8n 支援的 **Triggers**

---

## 1. **Trigger manually**

* **用途**：手動點擊「Execute workflow」執行。
* **使用時機**：

  * 測試或 Debug 工作流程。
  * 需要臨時人工觸發。

---

## 2. **On app event**

* **用途**：當第三方應用（如 Gmail、Slack、Telegram、Notion、Airtable 等）有事件發生時觸發。
* **使用時機**：

  * 例如 Gmail 收到新郵件 → 自動存到 Google Sheet。
  * Telegram 收到新訊息 → 觸發通知。

---

## 3. **On a schedule**

* **用途**：定時排程觸發（cron job）。
* **使用時機**：

  * 每天早上 9 點發 Slack 報告。
  * 每小時抓一次 API 更新數據。

---

## 4. **On webhook call**

* **用途**：當外部系統發送 HTTP 請求到 n8n Webhook URL 時觸發。
* **使用時機**：

  * 外部應用（ERP、CRM）呼叫 n8n API，將資料交給工作流。
  * Stripe / PayPal webhook 收款事件 → 自動觸發通知或入帳。

---

## 5. **On form submission**

* **用途**：提交 n8n 自建表單時觸發。
* **使用時機**：

  * 客戶填寫表單 → 自動建立 Google Drive 資料夾。
  * 支援內部 IT/HR 工單。

---

## 6. **When executed by another workflow**

* **用途**：被另一個工作流的 **Execute Workflow** 節點觸發。
* **使用時機**：

  * 將複雜流程拆分 → 多個子工作流，方便維護。
  * 例如：主流程 → 呼叫「寄送Email子流程」。

---

## 7. **On chat message**

* **用途**：當使用者在 n8n AI Chat 發送訊息時觸發。
* **使用時機**：

  * AI 客服 → 回答 FAQ。
  * AI 助理 → 接收輸入，觸發後續查詢。

---

## 8. **Other ways...**

* **用途**：其它觸發條件，例如：

  * Workflow error（錯誤時觸發）。
  * File change（檔案變更時觸發）。
* **使用時機**：

  * 工作流錯誤時 → 發 Slack 報警。
  * 檔案新增/修改 → 觸發自動處理。

---

📌 **總結建議**：

* **測試流程** → Trigger manually
* **自動化定時任務** → On a schedule
* **API / 第三方系統事件** → On webhook call / On app event
* **表單收集** → On form submission
* **模組化工作流** → When executed by another workflow
* **AI / Chatbot** → On chat message
* **錯誤監控或檔案監控** → Other ways

---

## **n8n Form Submission** 節點中常見欄位型別

### 📝 表單欄位型別說明

1. **Checkboxes（核取方塊）**

   * 允許使用者一次勾選一個或多個選項。
   * 適合用於多選題，例如「興趣」、「喜好功能」。

2. **Custom HTML（自訂 HTML）**

   * 可在表單中插入自訂 HTML 標籤或文字。
   * 常用來展示提示訊息、插入連結或說明文字，並非輸入欄位。

3. **Date（日期）**

   * 提供日期選擇器，讓使用者選擇一個日期。
   * 適合用於「生日」、「截止日期」、「活動日期」。

4. **Dropdown（下拉選單）**

   * 使用者從下拉清單中選擇一個或多個選項。
   * 適合用於「國家」、「部門」、「分類」等固定選項集合。

5. **Email（電子郵件）**

   * 專門用來輸入電子郵件地址，會自動驗證格式。
   * 適合用於收集使用者聯絡資訊。

6. **File（檔案上傳）**

   * 允許使用者上傳檔案（圖片、PDF、文件等）。
   * 適合用於「附件」、「履歷」、「證明文件」。

7. **Hidden Field（隱藏欄位）**

   * 使用者看不到，但提交時會包含固定值或系統產生的值。
   * 常用於傳遞內部 ID、追蹤碼或預設參數。

8. **Number（數字）**

   * 限制輸入為數字，支援整數或小數。
   * 適合用於「年齡」、「數量」、「價格」、「比率」。

9. **Password（密碼）**

   * 適合輸入密碼，內容會以隱藏符號顯示（●●●）。
   * 用於需要安全輸入的場合，例如帳號註冊或登入表單。

10. **Radio Buttons（單選按鈕）**

    * 使用者只能從多個選項中選擇一個。
    * 適合用於「性別」、「付款方式」、「是否同意」。

11. **Text（單行文字）**

    * 輸入單行文字內容。
    * 適合用於「姓名」、「標題」、「代碼」等短文字輸入。

12. **Textarea（多行文字區域）**

    * 輸入多行文字（支援換行）。
    * 適合用於「留言」、「描述」、「備註」。

---

## n8n 的 **節點 (nodes)** 分類及使用時機

### 1. **AI**

* **功能**：與 AI 模型互動，用於摘要、回答問題、RAG（檢索增強生成）、文件分析等。
* **使用時機**：

  * 需要 OpenAI/Anthropic 等模型做資料處理（例如 PDF 摘要、翻譯）。
  * 客服自動回覆、智慧助理、FAQ 自動應答。

---

### 2. **Action in an app**

* **功能**：對外部應用做動作，例如 **Google Sheets、Telegram、Notion、Gmail**。
* **使用時機**：

  * 新的 Gmail 收到 → 自動存到 Google Sheet。
  * Trello 卡片更新 → 同步到 Slack。
  * Notion 建立新頁面 → 自動建立資料庫紀錄。

---

### 3. **Data transformation**

* **功能**：對資料做 **轉換、過濾、格式化**。
* **使用時機**：

  * 把 JSON 轉成表格資料。
  * 過濾掉空值或重複的紀錄。
  * 把日期格式轉換成標準 ISO 格式。

---

### 4. **Flow**

* **功能**：控制流程，例如 **條件判斷 (If)、合併 (Merge)、迴圈 (Loop)**。
* **使用時機**：

  * 「如果」欄位值符合條件才往下執行。
  * 把兩個不同來源的資料合併成一個輸出。
  * 需要迴圈處理多個檔案或 API 回應。

---

### 5. **Core**

* **功能**：n8n 的基礎功能，例如 **HTTP 請求、Webhook、Run Code (JS/Python)**。
* **使用時機**：

  * 呼叫外部 API（POST/GET）。
  * 建立 Webhook 供第三方服務觸發流程。
  * 在節點中寫自定義的 Javascript/Python 處理邏輯。

---

### 6. **Human in the loop**

* **功能**：需要 **人工介入** 或 **人工審核** 的流程。
* **使用時機**：

  * 文件上傳後需要主管審核才能進入下一步。
  * RPA 自動處理流程中，某些高風險操作需要人工確認。

---

### 7. **Add another trigger**

* **功能**：一個 workflow 可以有 **多個觸發器**。
* **使用時機**：

  * 例如同一個流程可以由「Webhook 呼叫」或「排程」同時觸發。
  * 支援多種事件來源，但進入流程後會共用同一個工作流。

---

⚡ **總結：什麼時候用什麼？**

* **AI** → 要靠大語言模型處理內容。
* **Action in an app** → 跟外部應用整合（Google、Slack、Notion...）。
* **Data transformation** → 清洗資料、格式化。
* **Flow** → 條件判斷、合併、分支、迴圈。
* **Core** → Webhook、API、客製化程式邏輯。
* **Human in the loop** → 需要人工審核或輸入。
* **Add another trigger** → 一個 workflow 多事件入口。

---

## **n8n Data transformation節點類型與用途

### 🔥 Popular（常用）

* **🟧 Code**
  執行自訂 JavaScript 或 Python 程式碼。
  👉 用於需要自定義邏輯、轉換資料或調用外部 API。

* **🕒 Date & Time**
  處理日期與時間值，例如加減日期、格式轉換。
  👉 適合做任務排程或檔案命名加上時間戳。

* **✏️ Edit Fields (Set)**
  修改、增加或刪除資料項的欄位。
  👉 用於資料清洗或在流程中補充額外欄位。

---

### ➕ Add or remove items（新增或刪除項目）

* **🔎 Filter**
  過濾不符合條件的資料項。
  👉 用於只保留需要的資料。

* **⏬ Limit**
  限制輸出的資料筆數。
  👉 例如只要前 10 筆記錄。

* **🗑️ Remove Duplicates**
  刪除欄位值重複的項目。
  👉 避免重複紀錄進入資料庫。

* **🔀 Split Out**
  將清單中的元素拆分為獨立項目。
  👉 常用於 API 回傳陣列時，逐筆處理。

---

### 🔗 Combine items（合併項目）

* **📦 Aggregate**
  把多筆資料的某欄位合併成一個清單。
  👉 適合彙總結果，例如收集所有 email。

* **🔗 Merge**
  將多個資料流合併成一個。
  👉 適用於需要整合不同來源資料的情境。

* **🧮 Summarize**
  對資料進行統計（加總、計數、平均等）。
  👉 可用於報表或數據分析。

---

### 🔄 Convert data（資料轉換）

* **🗜️ Compression**
  壓縮或解壓縮檔案。

* **📂 Convert to File**
  將 JSON 資料轉換成二進制檔案。
  👉 常用於匯出報表或 API 上傳檔案。

* **🔑 Crypto**
  提供加密與雜湊功能。
  👉 可用於生成簽章或校驗值。

* **🖼️ Edit Image**
  編輯圖片（調整大小、加邊框等）。

* **📑 Extract from File**
  從二進制檔案中提取資料轉換成 JSON。
  👉 例如 PDF 解析。

* **🌐 HTML**
  操作 HTML 格式資料。

* **📝 Markdown**
  在 Markdown 與 HTML 之間轉換。

* **📄 XML**
  在 XML 與 JSON 間轉換。

---

### ⚙️ Other（其他）

* **✏️ Rename Keys**
  重新命名資料項的欄位。
  👉 適用於統一欄位名稱。

* **↕️ Sort**
  變更資料的排序順序。
  👉 可依照數字、文字或日期排序。

---

## 🔀 Flow 節點

### 🛠 Popular 節點

1. 🔎 **Filter**
   移除不符合條件的項目，用於資料篩選。

2. ➗ **If**
   根據布林條件 (true/false) 把流程分支。

3. 🔄 **Loop Over Items (Split in Batches)**
   將清單拆成批次，逐批處理，避免一次處理大量資料。

4. 🔗 **Merge**
   當兩個來源資料都準備好時，合併輸出。

---

### 🛠 Other 節點

1. ➕ **Compare Datasets**
   比較兩組輸入資料，檢查差異。

2. ↪️ **Execute Sub-workflow**
   呼叫另一個 n8n 工作流程，適合模組化或微服務設計。

3. ⚠️ **Stop and Error**
   停止工作流程並拋出錯誤。

4. 🔀 **Switch**
   根據條件或規則路由項目，類似多分支判斷。

5. ⏸ **Wait**
   暫停流程，直到條件滿足或時間到才繼續執行。

---
