# CASE STUDY 5 - Bank Customer Onboarding (Credit)

## 主流程

1. **开始事件**  
   - 流程从客户提交 **信用申请 (Credit Application)** 开始。

2. **自动获取信用分**  
   - 银行系统自动调用外部接口获取客户的 **Credit Score**。

3. **自动风险评估（业务规则任务）**  
   - 系统检查申请，确定风险等级。  
   - 三个互斥结果：  
     - **高风险 (Red)**  
       - 信用申请自动拒绝  
       - 发送拒绝通知给客户  
       - 流程以 **“Application Rejected”** 状态结束  
     - **无风险 (Green)**【默认路径】  
       - 信用申请自动接受  
       - 发送确认给客户  
       - 流程以 **“Application Accepted”** 状态结束  
     - **中等风险 (Yellow)**  
       - 需要人工审核（Manual Check 子流程）

---

## 子流程：Manual Check（人工审核）

1. **人工检查**（多步骤，可在独立图描述）  

2. **结果分支（互斥网关）**  
   - **通过** → 应用被接受 → 回到 **Green Path**  
   - **拒绝** → 应用被拒绝 → 回到 **Red Path**

3. **欺诈检测（中断边界事件）**  
   - 如果在人工检查过程中发现 **欺诈**：  
     - 中断人工审核  
     - 发送欺诈报告给监管/当局  
     - 申请以 **“Cancelled due to Fraud”** 状态结束
