下面把你列的工具（已校正拼寫：**JUnit 5、SonarQube、Snyk、OWASP（含 ZAP/Dependency-Check）、UiPath、JMeter、Veracode**）對應到你們的 4 個研發步驟，給出**最合適的用法與責任歸屬**。

---

# 工具對應一覽（按研發步驟）

## 1 Core development（Java / JS 核心研發）

**目的：** 把品質做進程式碼，早攔截、低成本。

* **單元/服務測試：** **JUnit 5**（Java 單元/服務層）、可配 Rest-Assured（API 層，仍用 JUnit 5 跑）。
* **靜態程式碼品質：** **SonarQube**（Java/JS 規則、異味、技術債、覆蓋率門檻）。
* **第三方依賴安全（SCA）：** **Snyk**（Java/JS 相依套件掃描、修補建議）。
* **元件/依賴弱點補充：** **OWASP Dependency-Check**（可與 Snyk並行；若工具疊床架屋，保留一個為阻斷門檻、另一個為告警）。
* **安全靜態掃描（SAST，選其一）：** **Veracode SAST**（如已購，將高風險設為阻斷）；若無則以 SonarQube 安全規則 + Snyk/SAST 取代。

> **CI Gate 建議（核心模組）**：Lint/SAST → JUnit 5（含覆蓋率）→ SonarQube Quality Gate → Snyk（阻斷高危）→ 允許合併

---

## 2 Baseline development（參數驅動的商務模組 JS）

**目的：** 讓規則/參數可測、可回歸、可審計。

* **規則/引擎輸出驗證：** **JUnit 5** 仍可作為「黑箱」測試執行器（呼叫 Baseline 的 API/函式，對比黃金樣本 Golden files）。
* **靜態品質/重複碼/異味：** **SonarQube**（針對 JS/TS 規則與覆蓋度）。
* **相依安全：** **Snyk**（JS 套件）。
* **基準差異/回歸：** 以 **JUnit 5** 驅動「資料驅動測試（CSV/JSON）」；結果落地為快照檔並納入 **SonarQube** 覆蓋率計算。
* **（可選）DAST 預檢**：若 Baseline 提供 Web 設定介面，可在 QA 前先用 **OWASP ZAP** 做輕量爬掃。

> **CI Gate 建議（Baseline 規則）**：Schema/Golden 驗證（JUnit 5）→ SonarQube → Snyk

---

## 3 QA（系統/端到端、效能、安全）

**目的：** 從使用者與端到端角度驗證可用性、效能與安全。

* **API/E2E 自動化：** 若已限定工具，API 仍用 **JUnit 5 + Rest-Assured**；UI 端若需錄放可借助 **UiPath**（RPA）覆蓋傳統/桌面/複雜流程（特別適合銀行內網或舊系統）。
* **效能/容量/耐久：** **JMeter**（壓測、峰值、P95/P99 指標）；測試腳本納 CI。
* **動態應用安全測試（DAST）：** **OWASP ZAP**（快速掃描）與/或 **Veracode Dynamic Analysis**（更完整的企業級 DAST）。
* **合規報告/治理：** **SonarQube**（整體品質門檻趨勢）、**Snyk**（開源相依風險趨勢）、**Veracode**（安全合規報告）。

> **CI/CD Gate 建議（QA 階段）**：部署至測試環境 → JUnit 5 API/冒煙 → JMeter（性能基線）→ ZAP/Veracode DAST（High=0）→ 產出測試與安全報告

---

## 4 Project development（基於 Baseline 的在地化整合）

**目的：** 快速客製 + 穩定對接外部（ESB/卡組織/KYC/風控等）。

* **整合/契約測試：** **JUnit 5 + Rest-Assured**（對各微服務/外部介面寫契約式 API 測試；若引入 CDC 工具受限，仍以 JSON 契約 + JUnit 5 驗證）。
* **效能/容量（整合維度）：** **JMeter**（針對介面與關鍵業務旅程壓測）。
* **安全/合規：** **Snyk**（新依賴掃描）、**OWASP ZAP/Veracode**（上線前的動態與組合掃描）。
* **排程式回歸/跨系統端到端：** **UiPath**（用 RPA 串起多系統手動場景，產可重播的 UAT 腳本）。
* **品質度量/治理：** **SonarQube**（專案支線也要有 Quality Gate；阻斷合併）。

> **放行條件（專案化發版）**：
> SonarQube 綠燈 + Snyk 高危=0 → JUnit 5 契約/回歸通過 → JMeter 達成 SLO → ZAP/Veracode 高危=0 → 變更核准

---

## 橫切與配置建議

* **唯一真相的 Quality Gate**：以 **SonarQube** 作為代碼與測試覆蓋的單一門檻；**Snyk/Veracode/ZAP** 負責安全阻斷；JMeter 提供效能門檻（P95、錯誤率）。
* **工具疊代減負**：Snyk（SCA）與 Veracode（SAST/DAST/SCA）職能有重疊——建議**選定一個作為阻斷（blocker），另一個作為佐證告警**，避免兩邊都阻斷造成流程摩擦。
* **報表與證跡**：把 **SonarQube、Snyk、Veracode、JMeter** 報告產物（HTML/XML/JSON）存入制品庫，方便 PMO 稽核與客戶交付。
* **UiPath 的定位**：將其用於**難以自動化的跨系統人工流程**（桌面/主機/舊式 Web），做為 UAT/回歸的「最後一哩」。
* **分層跑法（金字塔）**：大量 JUnit 5 單元 → 適量 API/契約（JUnit 5）→ 少量關鍵 E2E（UiPath/或留白）→ 效能（JMeter）→ 安全（ZAP/Veracode/Snyk）。

---

## 一張表總結

| 研發步驟             | 主要工具                                                                                                  | 用途/門檻                            |
| ---------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------- |
| Core (Java/JS)   | **JUnit 5**、**SonarQube**、**Snyk**、**OWASP Dependency-Check**、**Veracode SAST**                       | 單元/服務測試、品質門檻、相依掃描、SAST 阻斷        |
| Baseline (JS 規則) | **JUnit 5**、**SonarQube**、**Snyk**、（可選 **ZAP**）                                                       | 資料驅動/快照回歸、JS 品質與相依安全、介面預掃        |
| QA（系統/E2E/安全/效能） | **JUnit 5**（API 冒煙）、**UiPath**（跨系統 E2E）、**JMeter**、**OWASP ZAP**、**Veracode DAST**、**SonarQube/Snyk** | 端到端驗證、效能門檻、DAST、高危=0、品質趨勢        |
| Project（整合/客製）   | **JUnit 5 + Rest-Assured**、**JMeter**、**Snyk**、**ZAP/Veracode**、**UiPath**、**SonarQube**              | 契約/整合測試、介面效能、相依安全、RPA 回歸、品質 Gate |

---

## CI/CD 範本：含 **GitHub Actions** 與 **GitLab CI** 兩版（擇一即可）

### 目錄建議（Mono-repo 可參考）

```note
.
├─ backend/                 # Java (Maven/Gradle)
│  ├─ pom.xml
│  └─ src/test/java/...     # JUnit5 測試
├─ baseline/                # JS/TS 參數規則與黑箱測試
│  ├─ package.json
│  ├─ tests/...
│  └─ golden/...
├─ e2e/                     # ZAP/JMeter 腳本
│  ├─ zap-baseline.conf
│  └─ jmeter/*.jmx
└─ qa/                      # API 冒煙(JUnit5+Rest-Assured)等
```

---

### GitHub Actions（`.github/workflows/ci.yml`）

> 如用 GitLab，請跳到下一節。

```yaml
name: CI-Quality-Gates

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

permissions:
  contents: read
  security-events: write

env:
  # ---- Sonar ----
  SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
  SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  # ---- Snyk ----
  SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  # ---- Veracode ----
  VERACODE_API_ID: ${{ secrets.VERACODE_API_ID }}
  VERACODE_API_KEY: ${{ secrets.VERACODE_API_KEY }}
  VERACODE_APP_NAME: "My-App" # 依實際專案命名
  # ---- Service under test (for ZAP/JMeter) ----
  STAGING_BASE_URL: ${{ secrets.STAGING_BASE_URL }}

jobs:
  build-test-java:
    name: Core - Build & JUnit5 (Java)
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4

      - name: Setup JDK
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
          cache: 'maven'

      - name: Maven test (JUnit5) with reports
        run: mvn -B -DskipITs=false -DfailIfNoTests=false test

      - name: Package
        run: mvn -B -DskipTests package

      - name: Upload JUnit reports
        uses: actions/upload-artifact@v4
        with:
          name: junit-backend
          path: backend/target/surefire-reports/**/*.xml

  sonar:
    name: SonarQube / SonarCloud Analysis (blocker)
    runs-on: ubuntu-latest
    needs: [build-test-java]
    steps:
      - uses: actions/checkout@v4

      - name: Setup JDK for Sonar
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'

      - name: Sonar Scanner
        uses: SonarSource/sonarqube-scan-action@v3
        with:
          args: >
            -Dsonar.projectKey=my-app
            -Dsonar.sources=.
            -Dsonar.tests=backend/src/test,baseline/tests,qa
            -Dsonar.java.binaries=backend/target/classes
            -Dsonar.junit.reportPaths=backend/target/surefire-reports
            -Dsonar.javascript.lcov.reportPaths=baseline/coverage/lcov.info

      - name: Sonar Quality Gate (wait & fail if red)
        uses: SonarSource/sonarqube-quality-gate-action@v1.1.0
        with:
          timeout-minutes: 10

  snyk:
    name: Snyk SCA (blocker: high severity)
    runs-on: ubuntu-latest
    needs: [build-test-java]
    steps:
      - uses: actions/checkout@v4

      - name: Snyk Open Source scan (Java+JS)
        uses: snyk/actions/maven@master
        with:
          command: test --severity-threshold=high --fail-on=all-projects
        env:
          SNYK_TOKEN: ${{ env.SNYK_TOKEN }}

      - name: Snyk test for JS baseline
        uses: snyk/actions/node@master
        with:
          command: test --severity-threshold=high --file=baseline/package.json
        env:
          SNYK_TOKEN: ${{ env.SNYK_TOKEN }}

  zap:
    name: OWASP ZAP Baseline DAST (blocker: High=0)
    runs-on: ubuntu-latest
    needs: [build-test-java]
    steps:
      - uses: actions/checkout@v4

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.11.0
        with:
          target: ${{ env.STAGING_BASE_URL }}
          rules_file_name: e2e/zap-baseline.conf   # 可在此忽略非關鍵告警
          cmd_options: "-a"                         # 慎用：主動爬行增強覆蓋
      - name: Parse ZAP report (fail on high)
        run: |
          # 簡易示例：如需嚴格策略可用 jq 解析 report.json
          if grep -q "High (High)" report.md; then
            echo "High risk found by ZAP"; exit 1; fi
        shell: bash

      - name: Upload ZAP Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: zap-report
          path: |
            report.md
            zap_scan.log
            owasp_zap_report.html
          if-no-files-found: ignore

  jmeter:
    name: JMeter Performance Gate (P95, error rate)
    runs-on: ubuntu-latest
    needs: [build-test-java]
    steps:
      - uses: actions/checkout@v4

      - name: Run JMeter in Docker
        run: |
          mkdir -p perf-out
          docker run --rm -v $PWD/e2e/jmeter:/tests -v $PWD/perf-out:/out justb4/jmeter:5.6.3 \
            -n -t /tests/smoke.jmx -l /out/result.jtl -e -o /out/report

      - name: Simple Perf Gate (example)
        run: |
          python3 - << 'PY'
          import xml.etree.ElementTree as ET
          t = ET.parse('perf-out/result.jtl')
          s = t.getroot()
          samples = s.findall('httpSample') + s.findall('sample')
          errs = sum(1 for x in samples if x.attrib.get('s')=='false')
          tot  = len(samples) or 1
          err_rate = errs/tot
          # 假設將 P95 閾值/錯誤率做成常數；可改讀 report 指標
          if err_rate > 0.01:
              raise SystemExit(f"ERROR: error_rate={err_rate:.2%} > 1%")
          print("Perf gate passed")
          PY

      - name: Upload JMeter Report
        uses: actions/upload-artifact@v4
        with:
          name: jmeter-report
          path: perf-out/**

  veracode-sast:
    name: Veracode SAST (blocker: High=0)
    runs-on: ubuntu-latest
    needs: [build-test-java]
    steps:
      - uses: actions/checkout@v4
      - name: Build artifact (zip)
        run: |
          mkdir -p dist && cd backend
          mvn -B -DskipTests package
          cd ..
          zip -r dist/app.zip backend/target/*.jar baseline qa
      - name: Upload & Scan with Veracode
        uses: veracode/veracode-uploadandscan-action@v1.0.21
        with:
          vid: ${{ env.VERACODE_API_ID }}
          vkey: ${{ env.VERACODE_API_KEY }}
          appname: ${{ env.VERACODE_APP_NAME }}
          createprofile: true
          filepath: "dist/app.zip"
          scanpolling: 30
          scantimeout: 60
          failbuild: true
          criticality: "VeryHigh"

  veracode-dast:
    name: Veracode Dynamic (DAST) – optional blocker
    runs-on: ubuntu-latest
    needs: [zap]
    steps:
      - name: Veracode Dynamic Scan (placeholder)
        run: |
          echo "Trigger Veracode Dynamic Analysis against ${STAGING_BASE_URL}"
          echo "Use your org's CLI/API; set policy to fail on High=0"
```

### Secrets/變數需要設定

* `SONAR_HOST_URL`, `SONAR_TOKEN`
* `SNYK_TOKEN`
* `VERACODE_API_ID`, `VERACODE_API_KEY`, `VERACODE_APP_NAME`
* `STAGING_BASE_URL`（供 ZAP/JMeter 指向測試環境）

### 阻斷邏輯（重點）**

* **SonarQube Quality Gate**：紅燈即 fail。
* **Snyk**：`--severity-threshold=high --fail-on=all-projects`。
* **ZAP/Veracode**：如有 **High** 風險即 fail。
* **JMeter**：錯誤率 > 1% 即 fail（可依 SLO 調整並擴充 P95 門檻）。

---

### GitLab CI（`.gitlab-ci.yml`）

> 若你們用 GitLab，這版可直接用 **CI/CD Variables** 設定同名變數。

```yaml
stages:
  - build
  - test
  - quality
  - dast
  - perf
  - sast

variables:
  MAVEN_CLI_OPTS: "-B -DskipITs=false -DfailIfNoTests=false"
  SONAR_HOST_URL: "$SONAR_HOST_URL"
  SONAR_LOGIN: "$SONAR_TOKEN"
  STAGING_BASE_URL: "$STAGING_BASE_URL"

build_backend:
  stage: build
  image: maven:3.9-eclipse-temurin-21
  rules: [ { if: '$CI_COMMIT_BRANCH' } ]
  script:
    - cd backend
    - mvn $MAVEN_CLI_OPTS clean package
  artifacts:
    when: always
    paths:
      - backend/target
      - backend/target/surefire-reports
    expire_in: 7 days

unit_test_java:
  stage: test
  image: maven:3.9-eclipse-temurin-21
  needs: [ "build_backend" ]
  script:
    - cd backend
    - mvn $MAVEN_CLI_OPTS test
  artifacts:
    when: always
    reports:
      junit: backend/target/surefire-reports/*.xml
    expire_in: 7 days

sonar:
  stage: quality
  image: sonarsource/sonar-scanner-cli:latest
  needs: [ "build_backend", "unit_test_java" ]
  script:
    - sonar-scanner -Dsonar.projectKey=my-app
                    -Dsonar.host.url=$SONAR_HOST_URL
                    -Dsonar.login=$SONAR_LOGIN
                    -Dsonar.sources=.
                    -Dsonar.java.binaries=backend/target/classes
                    -Dsonar.junit.reportPaths=backend/target/surefire-reports

snyk:
  stage: quality
  image: snyk/snyk:latest
  needs: [ "build_backend" ]
  script:
    - snyk test --severity-threshold=high --all-projects
    - cd baseline && snyk test --severity-threshold=high
  rules:
    - if: '$SNYK_TOKEN'
  before_script:
    - export SNYK_TOKEN="$SNYK_TOKEN"

zap_baseline:
  stage: dast
  image: owasp/zap2docker-stable
  script:
    - zap-baseline.py -t "$STAGING_BASE_URL" -r zap.html -a -I
    - |
      if grep -q "High (High)" zap.html; then
        echo "ZAP found High risk"; exit 1; fi
  artifacts:
    when: always
    paths: [ "zap.html" ]

jmeter_perf:
  stage: perf
  image: docker:24.0.5
  services: [ "docker:24.0.5-dind" ]
  script:
    - apk add --no-cache python3
    - mkdir -p perf-out
    - docker run --rm -v $CI_PROJECT_DIR/e2e/jmeter:/tests -v $CI_PROJECT_DIR/perf-out:/out justb4/jmeter:5.6.3 \
        -n -t /tests/smoke.jmx -l /out/result.jtl -e -o /out/report
    - |
      python3 - << 'PY'
      import xml.etree.ElementTree as ET
      t = ET.parse('perf-out/result.jtl')
      s = t.getroot()
      samples = s.findall('httpSample') + s.findall('sample')
      errs = sum(1 for x in samples if x.attrib.get('s')=='false')
      tot  = len(samples) or 1
      if errs/tot > 0.01:
          raise SystemExit("Perf error rate >1%")
      print("Perf gate passed")
      PY
  artifacts:
    when: always
    paths: [ "perf-out" ]

veracode_sast:
  stage: sast
  image: cimg/base:stable
  needs: [ "build_backend" ]
  script:
    - sudo apt-get update && sudo apt-get install -y zip
    - mkdir -p dist && zip -r dist/app.zip backend/target/*.jar baseline qa
    - curl -sS https://downloads.veracode.com/securityscan/pipeline-scan-LATEST.zip -o ps.zip
    - unzip -q ps.zip -d veracode
    - java -jar veracode/pipeline-scan.jar \
        --veracode_api_id "$VERACODE_API_ID" \
        --veracode_api_key "$VERACODE_API_KEY" \
        --fail_on_severity "Very High, High" \
        --file "dist/app.zip"
  rules:
    - if: '$VERACODE_API_ID && $VERACODE_API_KEY'
```

---

### 補充建議（實務小訣竅）

* **把門檻「數字化」**：在 repo 放 `/.quality-gates.yml`，集中定義「覆蓋率、錯誤率、P95、High=0」等閾值，管線讀此檔，方便跨專案一致。
* **測試金字塔**：多跑 JUnit5 單元/契約；E2E 與 ZAP 保持**關鍵路徑**即可，降低 flakiness 與成本。
* **報表持久化**：所有報告（JUnit、Sonar、Snyk、ZAP、JMeter、Veracode）都上傳 artifacts，PMO 稽核/客戶交付一次到位。
* **避免重疊阻斷**：若 **Veracode** 已作為 SAST/DAST 主阻斷，**Snyk** 可作為 SCA 主阻斷；**ZAP** 作動態快速守門。明確主副工具，減少「雙重 fail」。

---
