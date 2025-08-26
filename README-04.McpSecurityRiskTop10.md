# 📋 MCP Security Risks Top 10 (中英文對照表)


| 序號     | 風險名稱 (中文)    | Risk Name (English)                   | 說明 (中文)                              | Description (English)                                                                             | 範例 (Example)                            |
| ------ | ------------ | ------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------- | --------------------------------------- |
| **1**  | 工具投毒         | Tool Poisoning                        | 惡意或被污染的 MCP 工具輸出錯誤資料，誤導決策。           | Malicious or poisoned MCP Tool returns incorrect/malicious data, misleading downstream workflows. | 惡意 `get_exchange_rate` 工具回傳錯誤匯率，導致交易錯誤。 |
| **2**  | Rockpools 攻擊 | Rockpools Attack                      | 攻擊者利用多個 MCP servers 間的依賴鏈，在其中插入惡意環節。 | Exploiting trust chains between MCP servers to insert a malicious “rock pool.”                    | OCR server 被篡改 → 合規檢查 server 誤判洗錢文件合法。  |
| **3**  | 地毯式詐騙        | Rug Pulls                             | MCP server 起初正常，取得信任後突然轉惡意。          | MCP server initially behaves normally but turns malicious after adoption.                         | Summarizer server 開始在摘要中注入釣魚連結。         |
| **4**  | 供應鏈注入        | Supply Chain Injection                | 攻擊者利用依賴套件或 API 植入惡意程式碼。              | Malicious code injected via package or downstream API dependencies.                               | 惡意 `pdf-parser` 套件導致伺服器執行後門。            |
| **5**  | 未授權工具執行      | Unauthorized Tool Execution           | Prompt Injection 或配置錯誤導致越權執行。        | Prompt injection or misconfig allows unauthorized tool calls.                                     | 文件查詢被誘導去調用「刪除文件工具」。                     |
| **6**  | 上下文洩漏        | Context Leakage                       | MCP 傳輸資料或日誌記錄洩露敏感內容。                 | Sensitive context exposed via logs, monitoring, or insecure transport.                            | 日誌伺服器將信用證 (LC) 文件內容上傳雲端。                |
| **7**  | 權限提升         | Privilege Escalation                  | 工具缺乏隔離，導致低權限工具竄升到高權限。                | Weak isolation allows escalation from low-privilege to high-privilege tool.                       | `doc_viewer` 被利用去呼叫 `system_shell`。     |
| **8**  | 拒絕服務攻擊       | Denial of Service (DoS)               | 攻擊者透過超大 payload 或高頻請求癱瘓 MCP。         | Large payloads or request floods overwhelm MCP server.                                            | 大量超大 JSON 請求癱瘓 `vector_db_upsert`。      |
| **9**  | 模型操縱 / 提示注入  | Model Manipulation / Prompt Injection | 攻擊者在上下文注入惡意指令，誘導錯誤輸出。                | Injecting malicious instructions into context to manipulate model/server.                         | 文件中隱藏「刪除所有資料」提示語。                       |
| **10** | 不安全配置與日誌     | Insecure Config & Logging             | 缺乏 TLS、認證、最小權限，或日誌過度暴露。              | Missing TLS/auth, over-logging, or weak config exposes system.                                    | MCP server 用 `http://` 公開，允許未授權調用。      |

---

✅ 這份表格可以當作 **MCP 版本的「OWASP Top 10」**，用於：

* **內部培訓**：教育開發與安全人員 MCP 風險。
* **審計清單**：針對每個風險設計控制措施。
* **紅隊測試**：模擬 Tool Poisoning、Rug Pull 等攻擊場景。

---

## MCP 安全風險

<https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks>

* TPA (Tool Poisoning Attack)
* RPA (Rug Pull Attack)
* CLP (Context Leakage)
* MMI (Model Manipulation Injection)
* RCE (Remote Code Execution)
* DoS (Denial of Service)
* RCE (Remote Code Execution)

## MCP Scan

<https://invariantlabs.ai/blog/introducing-mcp-scan>
<https://github.com/invariantlabs-ai/mcp-scan>

## MCP Security Scan Tools

<https://github.com/johnhalloran321/mcpSafetyScanner>
<https://github.com/General-Analysis/mcp-guard>
<https://github.com/invariantlabs-ai/mcp-scan>

## Legality

我幫你把圖片內容轉成文字：

1. Copyrights
2. Data Privacy *
3. Censorship *
    Censorship (審查) 的核心就是「限制或過濾資訊流通」。
4. License (such as n8n and Flowise)
5. Compliance

<https://console.groq.com/docs/legal>

## n8n **Sustainable Use License (SUL)**

### 📖 依據官方文件 (n8n Sustainable Use License)

👉 文件來源：
[https://docs.n8n.io/sustainable-use-license/#what-source-code-is-covered-by-the-sustainable-use-license]

### **Covered Code (受 SUL 限制的部分)**

* n8n 的 **核心程式碼 (Core Code)** 採用 **Sustainable Use License**。
* 意味著你可以 **免費使用、修改、部署** n8n，甚至用於商業環境。

---

### 📌 總結

* **免費 vs 收費**不是關鍵，關鍵在於：

  * 客戶是否能「直接使用」n8n 作為 workflow 平台？
  * 還是只是「間接受益」於 n8n 在後端的自動化？
* **只要客戶不能直接操作 n8n**，就不違反授權。
* **若客戶可以操作 n8n**（即使免費），就違反，需要商業授權。

---

### FlowiseAI 的授權限制

FlowiseAI 的核心原始碼是以 **Apache License 2.0** 授權，屬於開源授權模式。

這意味著：

* 你可以自由使用、修改、部屬 FlowiseAI。
* 允許商業使用，包括部署在 SaaS 或內部系統中。
* 只要遵守 Apache 2.0 的條款（保留原始授權資訊、記錄變更等），就不會違反授權。

---

### 自主部署 vs SaaS 提供的差異

根據第三方對 FlowiseAI 的總結：

* **Allowed（允許）**：自主部署 FlowiseAI 給客戶使用，並因為設定或建構工作收費。
* **Not Allowed（不允許）**：若你把 Flowise 打包成白標 SaaS 供人使用，或做成多租戶形式託管給客戶，**則違反 Apache 2.0 授權範圍**，除非你取得 FlowiseAI 團隊的商業授權。

---

### 簡表總結：FlowiseAI 授權 vs 行為限制

| 行為類型                     | 授權是否允許      | 說明                                                         |
| ------------------------ | ----------- | ---------------------------------------------------------- |
| 自主部署並提供給單一客戶使用           | 允許          | 與客戶合作部署、收取設定費或開發費皆可（Apache 2.0 規範內）。                       |
| 將 Flowise 作為 SaaS 供多租戶使用 | 不允許（除非商業授權） | 如果你作為平台托管，將 Flowise 作為「服務」提供給多名客戶，即使免費，也不符合 Apache 2.0 授權。 |

---

## 結語

* **FlowiseAI 採用 Apache 2.0 授權**，允許開源使用與修改。
* **自行部署給用戶使用** 是被允許的做法。
* **但若把 Flowise 用作白標 SaaS 或多租戶託管服務**，則需要額外洽談 FlowiseAI 團隊取得商業授權。

---

### ✅ 不受限制的情境

* **客戶自己安裝 / 自行部署 Flowise**：

  * 這完全屬於 **客戶自己使用開源軟體**，符合 Apache 2.0 授權。
  * 你只要提供 **整合 / 接口 / plugin**，讓客戶把你的 SaaS 與他們自己的 Flowise 環境對接，就不算你「轉售 Flowise」。
  * 所以這種情況 **不在限制之內**。

---

### 🔎 總結

* **你提供 SaaS = 不允許 (需要商業授權)**
* **客戶自己用 Flowise = 允許 (完全自由)**
* 你的角色可以是：

  * 提供 **integration connector**
  * 提供 **deployment 指南**
  * 或幫助客戶建置 Flowise 環境（收顧問費或維運費）。

---

### GDPR - 歐盟通用資料保護規章

Utilize GDPR compliance tools and frameworks (e.g., Botpress, Rasa, OneTrust) to streamline compliance.
