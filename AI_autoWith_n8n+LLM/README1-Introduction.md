# AI Automation with n8n and LLMs

## n8n vs Zapier 

### Features Comparison

| Feature                 | n8n               | Zapier                                                    |
| ----------------------- | ----------------- | --------------------------------------------------------- |
| Pre-built Connectors    | 387+              | 5,000+                                                    |
| Webhook Triggers        | Yes, on all plans | Premium app, available only with the Pro plan and onwards |
| Export/Import Workflows | Yes               | Yes                                                       |

### Pricing Comparison

| Plan    | n8n Cloud                            | Zapier                                  |
| ------- | ------------------------------------ | --------------------------------------- |
| Basic   | €20/mo for 2,500 workflow executions | €18.83/mo for 750 tasks (not workflows) |
| Premium | Varies based on usage                | Varies based on usage                   |

---

### 文字说明（右侧部分）

* n8n is better for **low-code** approach to building complex workflows fast
* Zapier is better for **no-code** approach handling simple tasks with a great range of integrations
* n8n is more cost effective to run with Cloud hosted and self hosted options available

---

## 比较 **n8n 和 Zapier** 两个自动化工具的差异

### 功能对比

* **预建连接器数量**：Zapier 拥有 **5000+**，远多于 n8n 的 **387+**。
* **Webhook 触发器**：n8n 在所有方案中都支持；Zapier 只有在 **Pro 及以上方案**才支持。
* **导入/导出工作流**：两者都支持。

### 价格对比

* **n8n Cloud 基础方案**：每月 €20，可执行 **2,500 个工作流**。
* **Zapier 基础方案**：每月 €18.83，但只包含 **750 个任务**（不是完整工作流）。
* **高级方案**：两者都依使用量而变化。

### 总结说明

* **n8n** 更适合 **低代码（low-code）** 场景，能快速构建复杂的工作流，并且支持云端托管和自托管，整体更具成本效益。
* **Zapier** 更适合 **无代码（no-code）** 场景，尤其是处理一些 **简单任务**，且拥有更广泛的集成范围。

---

## n8n Setup

```cmd
cd n8n-workflows
docker-compose up -d
```

## n8n Upgrade

```cmd
cd n8n-workflows
docker-compose pull
docker-compose down
docker-compose up -d
```

## n8n Templates

<https://n8n.io/workflows/>
