# SaaS Best Practices（Angular SPA + BFF + API Gateway + 微服務）

## 0. Executive Summary

* **選擇架構**：面向外部客戶的 SaaS → **SPA + BFF**；PoC/內部工具可接受 **純 SPA**。
* **核心原則**：Token 僅存 BFF、短壽命 AT、RT 旋轉、單例刷新、全線 RFC 7807、最小權限、觀測可追蹤。
* **錯誤處理**：預設不重試；僅 408/425/429 與 409/412 依規則一次重試（指數退避、尊重 `Retry-After`）。

---

## 1. Why SPA + BFF

**BFF（Backend For Frontend）** 讓前端不需持有 Token，將認證、授權、聚合、限流與可觀測集中到伺服器側：

* **安全性**：Token 不落地瀏覽器；HttpOnly + Secure + SameSite Cookie；可加 CSRF。
* **前端簡化**：無需處理 OAuth/OIDC 細節、刷新併發、Scope 管理。
* **治理一致**：Rate limit、審計、快取、A/B、風控在 BFF 施作；多端可共用。
* **可演進性**：BFF 可逐步導入 DPoP/mTLS、JWKS 輪換、零信任等增強措施。

---

## 2. Pure SPA vs SPA + BFF

| 面向        | 純 SPA（直打 API）               | SPA + BFF（推薦）                                           |
| --------- | --------------------------- | ------------------------------------------------------- |
| Token 存放  | 前端（memory/sessionStorage 等） | **僅在 BFF**；前端以 **HttpOnly+Secure+SameSite** Cookie 維持會話 |
| 安全性       | 易受 XSS 竊取 Token             | 前端不可讀 Token；搭配 CSRF 風險更低                                |
| 刷新        | 前端自行 refresh、需處理併發          | **BFF 代刷**；**RT Rotation + Reuse Detection**            |
| 授權/Scopes | 前端決定 scopes/audience        | BFF 依路由注入最小 scope/audience                              |
| CORS      | 跨域與預檢繁瑣                     | 同網域反代可基本免 CORS                                          |
| 限流/快取     | 主要在 Gateway                 | BFF 先分桶限流與快取，細粒度到租戶/使用者                                 |
| 稽核/追蹤     | 前端難帶全上下文                    | BFF 統一 `traceId`，涵蓋登入/刷新/撤銷                             |
| 登出        | 清本地狀態 + IdP logout          | BFF 銷毀會話 + IdP end session                              |
| 何時使用      | PoC／內部工具                    | 對外 SaaS／有安全與治理要求                                        |

---

## 3. SPA + BFF：Token 與 Refresh Token 最佳實踐

### 3.1 原則

* **Token 僅存 BFF**（伺服器/Redis），前端只持 **HttpOnly Cookie**。
* **AT 短壽命（5–15 分）**；**RT 旋轉 + Reuse Detection**（舊 RT 再用→立即撤銷會話）。
* **單例刷新**：同一會話一次僅允許一個 refresh 流程；其他請求等待結果。
* **雙超時**：Idle 30–60 分、Absolute 12–24 小時。
* **最小權限**：精準 `audience`、細粒度 `scope/role`。
* **撤銷/風控**：提供 `/logout`、`/revoke`；異常裝置/地理/RT 重用→強制登出。
* **金鑰治理**：KMS/HSM 管私鑰；JWKS + `kid` 輪換；可選 DPoP/mTLS。

### 3.2 標準流程

* **登入**：SPA → `/login` → BFF（Auth Code + PKCE）→ BFF 取得 AT/RT 並保存在服務端 → 設 HttpOnly Session Cookie。
* **呼叫 API**：SPA → `/api/*`（Cookie）→ BFF 注入 Bearer AT → 下游微服務。
* **預刷新**：AT < 2 分或 401(token\_expired) → BFF 用 RT 刷新（單例）→ 更新會話 → 重放原請求一次。
* **登出**：SPA → `/logout` → BFF 撤銷 RT、銷毀會話、IdP End Session → 204。

### 3.3 Cookie & CSRF

```note
Set-Cookie: sid=<opaque>; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=...
```

* 多子網/跨站需求：`SameSite=None; Secure` + CSRF（雙提交或自訂 header）。
* 嚴禁將 Token 放入 localStorage/sessionStorage。

---

## 4. SPA + BFF：400 系列（4xx）錯誤處理

### 4.1 統一契約

* **全線 RFC 7807（Problem+JSON）**：`type/title/status/detail/instance/traceId/errorCode/fields?`。
* **最小洩露**：不回堆疊；詳情留在日誌；以 `traceId/errorCode` 協助支援。
* **重試策略**：預設不重試；僅 **408/425/429** 與 **409/412** 依規則一次重試（**指數退避**、尊重 `Retry-After`）。

#### Problem+JSON 範例

```json
{
  "type": "https://docs.yourapp.com/errors/validation_failed",
  "title": "Validation failed",
  "status": 422,
  "detail": "email is invalid",
  "instance": "/api/v1/users",
  "traceId": "acme-3f2b...",
  "errorCode": "USR-VAL-001",
  "fields": {"email": "INVALID_FORMAT"}
}
```

### 4.2 伺服器何時回；BFF/SPA 怎麼做（精要表）

| 狀態碼         | 伺服器端         | BFF                               | SPA（Angular）            |
| ----------- | ------------ | --------------------------------- | ----------------------- |
| **400**     | 語法/格式/缺參     | 透傳                                | 表單高亮、不重試                |
| **401**     | 未驗證/Token 問題 | **僅**對 401 觸發刷新；Cookie 驗證失敗即回 401 | 觸發登入/刷新；同請求只重送一次        |
| **403**     | 權限不足         | 透傳                                | 顯示無權限，提供 CTA            |
| **404**     | 無路由/資源不存在    | 透傳（**勿**改 403）                    | 404 頁、清單空狀態             |
| **408**     | 逾時           | 標記可重試                             | 指數退避一次                  |
| **409/412** | 版本/條件衝突      | 推薦 `ETag/If-Match`                | 拉最新→合併→`If-Match` 重送一次  |
| **410**     | 永久移除         | `type` 指替代方案                      | 引導遷移                    |
| **422**     | 業務/欄位驗證      | 透傳 `fields`                       | 表單顯示、不重試                |
| **429**     | 限流/配額        | 補 `Retry-After`、`X-RateLimit-*`   | 指數退避一次，尊重 `Retry-After` |

> **400 vs 422**：格式/語法錯 → 400；業務驗證錯 → 422。
> **401 vs 403**：未驗證/Token → 401；已驗證但權限不足 → 403。

### 4.3 契約與標頭（高性價比）

* **併發控制**：回 `ETag`；更新需 `If-Match`；衝突回 409/412。
* **限流**：429 回 `Retry-After`、`X-RateLimit-Limit/Remaining/Reset`。
* **追蹤**：回 `X-Request-Id` 或在 Problem+JSON 放 `traceId`。
* **版本化/淘汰**：/v1；下線前用 **410** 並文件化替代方案。
* **安全**：`WWW-Authenticate` 明確 OAuth 錯因（`invalid_token`/`insufficient_scope`）。
* **CORS**：允許 `Authorization`；BFF/Cookie 場景支援 `withCredentials`。

### 4.4 前端（Angular）攔截器要點（示意）

```ts
catchError((err: HttpErrorResponse) => {
  const p = err.error as any; // RFC7807
  switch (err.status) {
    case 400:
    case 422: form.showFieldErrors(p.fields); break;
    case 401: return auth.retryOnceWithLogin(req, next);
    case 403: ui.warn('沒有權限'); break;
    case 404:
    case 410: router.navigate(['/404']); break;
    case 408:
    case 425:
    case 429: return retryWithBackoffOnce(err, p?.['retry-after']);
    case 409:
    case 412: return refetchMergeAndRetry(req, next, p);
  }
  return throwError(() => err);
});
```

---

### 5. 觀測、稽核與風控（Others）

* **全鏈路追蹤**：每請求 `traceId`；登入/刷新/撤銷/授權拒絕事件入庫。
* **爆量監控**：4xx 速率、租戶/路由分桶趨勢；暴增＝前端 bug 或攻擊訊號。
* **冪等性**：對可能重試的變更操作使用 **`Idempotency-Key`**。
* **Webhook 安全**：用 HMAC/Ed25519 簽名 + 時戳 + 回放防護（不要用 Bearer）。
* **密鑰管理**：私鑰置於 KMS/HSM；JWKS 發佈與輪換流程；密鑰退場計畫（重疊期/雙簽）。
* **隱私**：最小化 PII；Token/日誌脫敏；設定資料保存期限與刪除機制。

---

### 6. 一頁落地檢查表

* [ ] 前端只用 **HttpOnly Session Cookie**；Token 全在 BFF
* [ ] AT 5–15 分；**RT Rotation + Reuse Detection**；**單例刷新**
* [ ] Idle/Absolute 超時；CSRF（SameSite + 雙提交或自訂 header）
* [ ] Gateway/微服務驗簽與最小 scope；**RFC 7807** 全線上線
* [ ] 429：`Retry-After`、`X-RateLimit-*`；變更接口：`ETag/If-Match`、`Idempotency-Key`
* [ ] 4xx 全部集中日誌；`tenantId/userId/traceId` 分桶報表與告警
* [ ] 版本與淘汰策略（410）；多租戶不洩漏資源存在性
* [ ] KMS/HSM、JWKS 輪換、Webhook 簽名、CSP/Trusted Types

---

## 📖 RFC 7807 `application/problem+json` 400 系列錯誤範例

### 400 Bad Request（請求格式錯誤）

```json
{
  "type": "https://docs.saas.com/errors/bad_request",
  "title": "Bad Request",
  "status": 400,
  "detail": "JSON payload is malformed.",
  "instance": "/api/v1/users",
  "traceId": "req-abc123",
  "errorCode": "USR-REQ-001"
}
```

---

### 401 Unauthorized（未授權 / Token 過期）

```json
{
  "type": "https://docs.saas.com/errors/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Access token is expired or missing.",
  "instance": "/api/v1/orders",
  "traceId": "req-xyz789",
  "errorCode": "AUTH-401",
  "wwwAuthenticate": "Bearer realm=\"saas-api\", error=\"invalid_token\", error_description=\"The access token expired\""
}
```

---

### 403 Forbidden（越權存取）

```json
{
  "type": "https://docs.saas.com/errors/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "You do not have permission to access this resource.",
  "instance": "/api/v1/admin/settings",
  "traceId": "req-233aaa",
  "errorCode": "AUTH-403"
}
```

---

### 404 Not Found（資源不存在）

```json
{
  "type": "https://docs.saas.com/errors/not_found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "User with id=12345 does not exist.",
  "instance": "/api/v1/users/12345",
  "traceId": "req-777eee",
  "errorCode": "USR-NOT-FOUND"
}
```

---

### 408 Request Timeout（請求逾時）

```json
{
  "type": "https://docs.saas.com/errors/request_timeout",
  "title": "Request Timeout",
  "status": 408,
  "detail": "The request took too long to complete.",
  "instance": "/api/v1/upload",
  "traceId": "req-555mmm",
  "errorCode": "TIMEOUT-408",
  "retryAfter": 5
}
```

---

### 409 Conflict（資源衝突）

```json
{
  "type": "https://docs.saas.com/errors/conflict",
  "title": "Conflict",
  "status": 409,
  "detail": "Update conflict: resource has been modified by another request.",
  "instance": "/api/v1/invoices/567",
  "traceId": "req-111bbb",
  "errorCode": "INV-CONFLICT",
  "conflictVersion": "etag-20240901"
}
```

---

### 410 Gone（資源已刪除/廢棄）

```json
{
  "type": "https://docs.saas.com/errors/gone",
  "title": "Gone",
  "status": 410,
  "detail": "This API endpoint is deprecated. Use /api/v2/reports instead.",
  "instance": "/api/v1/reports",
  "traceId": "req-222ccc",
  "errorCode": "API-DEPRECATED"
}
```

---

### 412 Precondition Failed（前置條件失敗）

```json
{
  "type": "https://docs.saas.com/errors/precondition_failed",
  "title": "Precondition Failed",
  "status": 412,
  "detail": "ETag mismatch. The resource was modified.",
  "instance": "/api/v1/files/123",
  "traceId": "req-444ddd",
  "errorCode": "FILE-ETAG-MISMATCH",
  "expectedETag": "abc123",
  "providedETag": "xyz999"
}
```

---

### 413 Payload Too Large（上傳內容超過限制）

```json
{
  "type": "https://docs.saas.com/errors/payload_too_large",
  "title": "Payload Too Large",
  "status": 413,
  "detail": "Upload size exceeds limit of 10MB.",
  "instance": "/api/v1/upload",
  "traceId": "req-999kkk",
  "errorCode": "UPLOAD-LIMIT",
  "maxSize": "10MB"
}
```

---

### 415 Unsupported Media Type（媒體格式不支援）

```json
{
  "type": "https://docs.saas.com/errors/unsupported_media_type",
  "title": "Unsupported Media Type",
  "status": 415,
  "detail": "Only application/json is supported.",
  "instance": "/api/v1/orders",
  "traceId": "req-888jjj",
  "errorCode": "MEDIA-UNSUPPORTED",
  "supportedTypes": ["application/json"]
}
```

---

### 422 Unprocessable Entity（業務驗證失敗）

```json
{
  "type": "https://docs.saas.com/errors/validation_failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Invalid email address provided.",
  "instance": "/api/v1/users",
  "traceId": "req-666ppp",
  "errorCode": "USR-VAL-001",
  "fields": {
    "email": "INVALID_FORMAT"
  }
}
```

---

### 429 Too Many Requests（流量過高）

```json
{
  "type": "https://docs.saas.com/errors/too_many_requests",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "Rate limit exceeded. Please try again later.",
  "instance": "/api/v1/search",
  "traceId": "req-1010rrr",
  "errorCode": "RATE-LIMIT",
  "retryAfter": 30,
  "rateLimit": {
    "limit": 100,
    "remaining": 0,
    "reset": "2025-09-14T12:00:00Z"
  }
}
```

---

✅ **總結**
這些範例都遵循 **RFC 7807**，並額外加上 `traceId`、`errorCode`、`fields` 等實務 SaaS 常用欄位，方便 **前端 UX 提示** 與 **後端追蹤排錯**。
