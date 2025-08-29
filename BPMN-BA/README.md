# BPMN

## BPMN Tools

- ADONIS:Community Edition (adonis-community.com).
- Create and export it to BPMN VSC extension BPMN.io Editor (bpmn.io). **

## BPMN + n8n

BPMN 和 n8n 結合，可以形成互補，發揮「業務流程建模」與「技術自動化」的雙重優勢。

---

### 1. 業務流程層（BPMN）

在 BPMN 中定義完整業務工作流，包含人工節點（User Task、Manual Task）和自動化節點（Service Task）。  

**流程範例：**

- **Step1: 業務員輸入資料（User Task）**  
  人工輸入申請資料。

- **Step2: 系統自動調用 API 做合規檢查（Service Task → n8n Workflow）**  
  由 n8n 執行黑名單檢查、KYC、AML 過濾等。

- **條件判斷（Exclusive Gateway）**  
  - 若檢查通過：直接跳過人工審批，進入 Step4。  
  - 若檢查不通過：流轉到 Step3 進行人工審批。  

- **Step3: 合規人員人工審批（User Task）**  
  僅在自動檢查有問題時觸發，供合規人員人工介入。  

- **Step4: 系統自動發送結果給核心系統（Service Task → n8n Workflow）**  
  由 n8n 執行資料落地、通知、Email 等後續動作。  

---

### 2. 自動化執行層（n8n）

- BPMN 中的 **Service Task** 可對應到 **n8n Workflow URL** 或 **Webhook**。  
- n8n 負責技術自動化，包括 API 呼叫、資料庫操作、Email 發送、檔案處理等。  
- 最後將結果回傳 BPMN 引擎（如 Camunda、Flowable），由 BPMN 決定後續流程（是否進人工審批或結束）。  

---

### 3. 效益

- **人工 + 自動化最佳結合** → 人工審批交給 BPMN，自動化交給 n8n。  
- **合規與審計** → BPMN 流程圖可直接用於內部審計與監管報告。  
- **靈活性** → n8n 流程可隨時調整，不必修改 BPMN 模型。  
- **降低成本** → 業務人員與技術人員各自專注於專業領域。  

**額外好處：**

- **效率提升**：大部分合規檢查可自動完成，減少人工干預。  
- **合規保護**：疑慮案例才交由人工審批，確保風險可控。  
- **可審計**：BPMN 圖清楚展示「自動通過」與「人工審批」兩條路徑。  

---
