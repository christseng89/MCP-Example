# BPMN 命名约定最佳实践

## 概述

业务流程建模与标记法 (BPMN) 命名约定对于创建清晰、易懂和可维护的流程模型至关重要。本指南概述了命名 BPMN 元素的最佳实践。

## 核心原则：**动词 + 名词**

BPMN 活动的主要命名约定是**"动词 + 名词"**，这提供了清晰和面向行动的描述。

## 元素特定命名约定

### 🔷 活动/任务：动词 + 名词

**模式**：`[动作动词] + [对象/名词]`

**✅ 好的例子：**

- 处理发票 (Process Invoice)
- 批准请求 (Approve Request)
- 发送邮件 (Send Email)
- 审核申请 (Review Application)
- 创建报告 (Create Report)
- 更新数据库 (Update Database)
- 验证数据 (Validate Data)
- 生成发票 (Generate Invoice)

**❌ 不好的例子：**

- 发票处理 (Invoice Processing)
- 请求批准 (Request Approval)
- 邮件发送 (Email Sending)
- 申请审核 (Application Review)

### 🔴 事件：名词 + 过去分词/状态

**开始事件：**

- 客户投诉 (Customer Complaint)
- 订单请求 (Order Request)
- 付款到期 (Payment Due)

**结束事件：**

- 发票已发送 (Invoice Sent)
- 流程已完成 (Process Completed)
- 请求被拒绝 (Request Rejected)
- 订单已完成 (Order Fulfilled)

**中间事件：**

- 收到付款 (Payment Received)
- 批准超时 (Approval Timeout)
- 文档已更新 (Document Updated)
- 发生错误 (Error Occurred)

### 🔶 网关：问题

**模式**：明确的是/否问题或决策标准

**✅ 好的例子：**

- 金额 > ¥10000？ (Is Amount > ¥10000?)
- 已批准？ (Approved?)
- 付款方式？ (Payment Method?)
- 客户类型？ (Customer Type?)
- 风险级别高？ (Risk Level High?)
- 文档有效？ (Valid Document?)

### 📄 数据对象：名词

**模式**：清晰、具体的名词

**✅ 好的例子：**

- 发票 (Invoice)
- 客户数据 (Customer Data)
- 批准表单 (Approval Form)
- 采购订单 (Purchase Order)
- 付款收据 (Payment Receipt)
- 合同文档 (Contract Document)

### 🏊 池和泳道：组织单位

**模式**：角色或部门名称

**✅ 好的例子：**

- 客户服务 (Customer Service)
- 财务部门 (Finance Department)
- 销售团队 (Sales Team)
- IT支持 (IT Support)
- 外部供应商 (External Vendor)

## 关键原则

### 1. **面向行动**

活动应该清楚地表明正在执行什么行动，使流程流向直观。

### 2. **简洁**

保持名称简短但具有描述性（最多2-4个词）。避免不必要的冠词和介词。

### 3. **业务语言**

使用业务利益相关者熟悉的术语，而不是技术术语。

### 4. **一致性**

在整个流程模型中应用相同的命名模式，以提高可读性。

### 5. **具体性**

在保持简洁的同时，要足够具体以避免歧义。

### 6. **标准化**

遵循组织的命名标准和约定。

## 常见错误避免

### ❌ 动名词形式 (-ing)

- **错误**: "正在处理发票" ("Processing Invoice")
- **正确**: "处理发票" ("Process Invoice")

### ❌ 被动语态

- **错误**: "发票被处理" ("Invoice is Processed")
- **正确**: "处理发票" ("Process Invoice")

### ❌ 模糊术语

- **错误**: "处理请求" ("Handle Request")
- **正确**: "批准请求" ("Approve Request") 或 "审核请求" ("Review Request")

### ❌ 技术术语

- **错误**: "执行SQL查询" ("Execute SQL Query")
- **正确**: "检索客户数据" ("Retrieve Customer Data")

## 按行业分类的示例

### 金融服务

- **活动**: 处理贷款、验证身份、计算利息
- **事件**: 收到付款、开户完成、检测欺诈
- **网关**: 信用评分 > 700？、贷款已批准？

### 医疗保健

- **活动**: 预约安排、审核病史、开处方药
- **事件**: 患者入院、测试结果可用、授权出院
- **网关**: 紧急情况？、保险覆盖？

### 制造业

- **活动**: 组装产品、质量检查、发货订单
- **事件**: 原材料到达、生产完成、发现缺陷
- **网关**: 质量通过？、库存可用？

## 工具和实施

### 建模工具设置

- 在 BPMN 工具中配置命名模板
- 设置命名验证规则
- 使用一致的字体和格式

### 团队指导原则

- 创建命名约定检查清单
- 定期进行模型评审
- 维护批准术语词汇表

## 良好命名约定的好处

1. **改进沟通** - 利益相关者能快速理解流程
2. **更好维护** - 更容易更新和修改流程
3. **减少错误** - 清晰命名防止误解
4. **增强自动化** - 促进流程自动化实施
5. **合规支持** - 帮助审计和监管要求

## 结论

遵循 BPMN 活动的**"动词 + 名词"**约定，结合其他元素的适当命名模式，可以创建以下特点的流程模型：

- 易于阅读和理解
- 快速导航
- 简单维护
- 可自动化

## 记住

良好的命名约定是对流程建模计划长期成功的投资。

---

最后更新：2024年12月
