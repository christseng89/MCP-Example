# 本機運行的 n8n 能夠存取 Google Sheets

## **第一部分：設定 Google Cloud 專案**

### 1. 登入 Google Cloud Console

* 開啟 [Google Cloud Console](https://console.cloud.google.com)。
* 使用你要存取 Google Sheets 的 Google 帳號登入。

### 2. 建立新專案

* 在頂部導航列點選專案下拉選單（如果之前用過，可能會顯示 "mcp-buildagents"）。
* 選擇「新專案」。
* 輸入專案名稱，例如 `mcp-buildagents`。
* 點「建立」。
* 專案建立後，確保在專案下拉選單中已選中該專案。

### 3. 啟用 Google Sheets API

* 在 Google Cloud Console 左側選單進入 **「API 和服務」>「資料庫」**。
* 搜尋「Google Sheets API」並按 Enter。
* 點選搜尋結果中的 **Google Sheets API**。
* 點「啟用」。
* （可選）如果 n8n 工作流程還要管理檔案或權限（如上傳檔案），重複以上步驟啟用 **Google Drive API**。

### 4. 設定 OAuth 同意畫面

* 左側選單進入 **「API 和服務」>「OAuth 同意畫面」**。
* **使用者類型**：選擇「External」並點「建立」，允許任何 Google 帳號授權。
* **應用程式註冊**：

  * 應用名稱：輸入如「mcp build agents」。
  * 使用者支援電子郵件：選擇你的電子郵件。
  * 開發人員聯絡資訊：輸入你的電子郵件。
  * 點「儲存並繼續」。
* **範圍 (*Scopes*)**：

  * 點「新增或移除範圍」。
  * 搜尋「Google Sheets」並選擇需要的範圍（例如 `.../auth/spreadsheets`）。
  * 如果已啟用 Google Drive API，也可加入 `.../auth/drive`。
  * 點「更新」→「儲存並繼續」。
* **測試使用者 (*Audience*)**：

  * 點「新增使用者」，輸入將用來連接 n8n 的 Google 帳號（與登入 Cloud Console 的帳號相同）。
  * 點「新增」→「儲存並繼續」。
* **摘要**：檢查設定並點「返回主控台」。

### 5. 建立憑證（OAuth 用戶端 ID）

* 左側選單進入 **「API 和服務」>「憑證」**。
* 點「建立憑證」→「***OAuth 用戶端 ID***」。
* 應用類型：選擇「網路應用程式」。
* 名稱：例如「mcp build agents」。
* 授權重新導向 URI：稍後填入從 n8n 取得的 URI（先保持此頁開啟）。

---

## **第二部分：在 n8n 中整合 Google Sheets**

### 1. 開啟 n8n

* 在本機啟動 n8n。

### 2. 新增 Google Sheets 節點

* 在 n8n 工作流編輯器點「+」新增節點。
* 搜尋「Google Sheets」並選擇 **Google Sheets** 節點。

### 3. 建立憑證

* 在節點設定中，找到「Credential to connect with」欄位，選擇「建立新憑證」。
* 選擇 **Google Sheets OAuth2 API**。

### 4. 從 n8n 取得重新導向 URI

* 在憑證設定視窗中，複製「OAuth Redirect URL」。

### 5. 將 Redirect URI 填入 Google Cloud Console

* 回到 Cloud Console 建立 OAuth 用戶端 ID 的頁面。
* 在「授權重新導向 URI」中點「+新增 URI」，貼上剛才從 n8n 複製的網址。
* 點「建立」。
* 彈出視窗會顯示 **Client ID** 和 **Client Secret**，將它們複製。

### 6. 回到 n8n 完成憑證設定

* 在 n8n 憑證設定中，將 **Client ID** 和 **Client Secret** 貼入相應欄位。
* 點「儲存」。

### 7. 授權連線

* 儲存後，n8n 會顯示「Sign in with Google」按鈕。
* 點選並用你在測試使用者清單中的 Google 帳號登入。
* Google 會顯示授權畫面，點「允許」。
* 成功後視窗會關閉，n8n 顯示已連線成功。

### 8. 設定 Google Sheets 節點

* 選擇剛建立的憑證。
* 選擇操作類型（例如「讀取表格」、「新增列」、「更新列」）。
* 輸入 Spreadsheet ID（可從 Google Sheets 網址取得）與 Sheet Name。

---

完成後，本機運行的 n8n 就能成功存取 Google Sheets 了 ✅
