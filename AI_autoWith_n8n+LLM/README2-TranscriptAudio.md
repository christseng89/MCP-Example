# Transcript Audio

## 什么是 LangChain？

**“链（chain）”** 不同的组件在一起，用来创建更高级的用例。

* 🔗 **基础 LLM 链（Basic LLM Chain）**
  一个简单的链，用来调用大型语言模型。

* 🔗 **问答链（Question and Answer Chain）**
  根据检索到的文档回答问题。

* 🔗 **总结链（Summarization Chain）**
  将文本转换为简洁的总结。

---

👉 总结：LangChain 的核心思想就是 **把不同功能模块“串联”起来**，让大模型不仅能回答单一问题，还能处理复杂任务，例如 **提示调用 → 文档检索 → 问答 → 总结**。

## 什么是 Agent？

**Agent（智能体）** 在概念上是把 **大型语言模型（LLM）** 与 **工具、提示（Prompt）和记忆（Memory）** 结合起来。

### 常见类型

* **会话型 Agent（Conversational Agent）**
  选择合适的工具来完成任务，并利用记忆回忆之前的对话内容。

* **OpenAI Functions Agent**
  使用 OpenAI 的 Function Calling 功能来选择合适的工具，并传递参数执行任务。

* **计划与执行 Agent（Plan and Execute Agent）**
  先制定计划，决定要做什么，然后执行子任务以达成目标。

* **ReAct Agent**
  战略性地选择工具来完成特定任务。

---

👉 总结：Agent 就是一个 **智能执行体**，它不仅能调用大模型生成回答，还能结合外部工具、记忆和推理策略，完成更复杂的任务。

---

## **LangChain 和 Agent 的不同点**

### 1. 定义层面

* **LangChain**
  是一个 **框架**，主要目标是把 **LLM（大语言模型）和外部资源**（比如数据库、API、向量库）“串联”起来，形成更复杂的 **链式工作流（Chain）**。

* **Agent**
  是一种 **运行时的执行体**，它把 **LLM + 工具 + 记忆 + 提示** 结合起来，可以 **动态决策**：选择要调用哪个工具、如何拆解任务、以及如何执行。

---

### 2. 工作方式

* **LangChain Chain（链）**

  * 预先定义好流程，比如：
    **用户问题 → 文档检索 → LLM 总结 → 输出**。
  * 流程是 **固定的**，一步步按顺序执行。

* **Agent（智能体）**

  * 没有固定流程，而是通过 LLM 的推理来 **动态决定**：

    * 要不要调用某个工具？
    * 调用哪个 API？
    * 如何把任务拆分成子任务？
  * 更像是 **自主调度员**。

---

### 3. 应用场景

* **LangChain**

  * 适合 **可预测、结构化的任务**。
  * 例如：问答链、总结链、翻译链。

* **Agent**

  * 适合 **复杂、开放式的任务**，需要推理和决策。
  * 例如：

    * 自动化研究助手（先搜索资料，再总结）。
    * 智能客服（决定何时调用数据库、何时回答）。
    * 工作流执行器（自动选择工具完成任务）。

---

### 4. 对比总结表

| 维度  | LangChain     | Agent                |
| --- | ------------- | -------------------- |
| 本质  | 框架，用来构建“链”    | 执行体，结合 LLM + 工具 + 记忆 |
| 流程  | 固定链式，预定义步骤    | 动态决策，按需选择工具          |
| 复杂度 | 简单到中等         | 中高复杂度                |
| 应用  | 文本处理、问答、总结    | 自主研究、任务拆解、复杂决策       |
| 类比  | **流水线**（固定顺序） | **经理人**（根据情况灵活分配任务）  |

---

✅ **一句话总结**：
LangChain 提供了“搭积木”的框架，适合构建链式任务；而 Agent 是一个“智能执行者”，适合在复杂环境中动态选择工具和路径。

---

### ✅ 更精確的理解

* **LangChain** = 搭積木的 **框架**

  * 提供各種「積木」（例如：Prompt 模板、LLM 接口、記憶體、工具、向量資料庫整合…）。
  * 你可以把這些積木 **自由組裝成固定流程（Chains）**。
  * 它本身不決定「怎麼用」，只是提供建材 + 拼裝方法。

* **Agent** = 利用積木拼出來的一種「智慧應用」

  * 它不只是一個組裝好的功能，而是一種 **動態決策的模式**。
  * 它用 LangChain 的積木（LLM + 工具 + 記憶 + Prompt），再加上「推理邏輯」（比如 ReAct、Plan-and-Execute），變成一個能**自己判斷**「下一步要怎麼走」的**智能體**。

---

### 🔍 舉例

* **Chain（鏈）** → 就像「自動咖啡機」：流程固定，按下按鈕 → 磨豆 → 萃取 → 倒咖啡。
* **Agent（智能體）** → 就像「咖啡師」：客人點單後，會判斷要不要加奶泡、要不要先磨冰塊、選哪個杯子，步驟是 **靈活的**。
* **LangChain** → 提供了「咖啡豆、奶泡機、冰塊機、菜單設計圖」，你自己組裝出自動機器，或訓練咖啡師去用。

---

✅ 所以可以說：

* LangChain = **基礎框架/積木**
* Chains = **固定流程的組裝成品**
* Agents = **更高階的組裝成品**（會**動態選擇流程**的智能應用）

---

## Transcript Audio 工作流

* 🔗 **转录 → 总结 → 翻译 → 生成音频

### 工作流步骤

1. **当点击 "Test workflow"** or **Google Drive Trigger**
   （触发器/Automatically run when a file is added in a folder in Google Drive）

2. **Google Drive**
   下载文件

3. **OpenAI**
   转录录音

4. **Summarize Transcription**
   总结转录内容
   （调用 OpenAI Chat Model）

5. **Translate to Japanese**
   翻译成日语
   （调用 OpenAI Chat Model）

6. **Generate Audio**
   生成音频 (OpenAI Whisper)

7. **Google Drive1**
   上传文件

---

👉 总结：
这个工作流会先 **从 Google Drive 获取音频 → 转录 → 总结 → 翻译 → 生成音频 → 上传回 Google Drive**。

## Google Drive Setup

* From n8n => Google Drive Trigger => Create New Credential => OAuth Redirect URL 
  *<http://localhost:5678/rest/oauth2-credential/callback>
* Google Cloud Console <https://console.cloud.google.com/>
  * Create Project (mcp-buildagents)
  * APIs & Services => Enable APIs & Services => Google Drive API/Gmail API/Google Calendar API
  * Create OAuth 2.0 Client IDs
    * Application Type: Web Application
    * Authorized redirect URIs: <http://localhost:5778/rest/oauth2-credential/callback>
    * Create Client Secret
  * Download JSON file
  * Open JSON file and copy Client ID and Client Secret to n8n Google Drive Credential

## n8n flows

*01.1 Transcribe Audio to Text v1 (home)
*01.1 Transcribe Audio to Text v2 (folder)
*01.2 Transcribe Audio fr En to Cn
