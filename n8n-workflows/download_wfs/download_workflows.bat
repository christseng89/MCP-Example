@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ===== Config =====
set BASE=http://localhost:5778
set EMAIL=samfire5200@gmail.com
set PASS=t0210#Chris

REM Login and save session cookie
curl.exe -s -X POST %BASE%/rest/login ^
  -H "Content-Type: application/json" ^
  -d "{\"emailOrLdapLoginId\":\"%EMAIL%\",\"password\":\"%PASS%\"}" ^
  --cookie-jar cookies.txt > nul

REM ===== 0) 檢查必要檔 =====
if not exist cookies.txt (
  echo [ERROR] cookies.txt 不存在，請先用 /rest/login 取得登入 cookie
  exit /b 1
)

REM ===== 1) 取全部 workflows 清單到 workflows.json =====
echo Fetching workflows list...
curl.exe -s -b cookies.txt "%BASE%/rest/workflows" -o "workflows.json"

REM ===== 2) 由 workflows.json 產生 id|sanitized_name 對照表 map.txt =====
REM 使用 PowerShell 解析 JSON 並移除 Windows 不允許的檔名字元 <>:"/\|?*
powershell -NoProfile -Command ^
  "$w=(Get-Content 'workflows.json' -Raw | ConvertFrom-Json).data; " ^
  "$w | ForEach-Object { $n=$_.name -replace '[<>:""/\\|?*]','_'; $n=$n.Trim(); " ^
  "  if([string]::IsNullOrWhiteSpace($n)){ $n = 'workflow_' + $_.id } ; " ^
  "  Write-Output ($_.id + '|' + $n) }" ^
  > map.txt

if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] 解析 workflows.json 失敗
  exit /b 1
)

REM ===== 3) 逐一下載：以「名稱」命名檔案 =====
echo Exporting each workflow as its real name...
for /f "usebackq tokens=1,2 delims=|" %%A in ("map.txt") do (
  set "ID=%%A"
  set "NAME=%%B"
  set "OUT=%%B.json"

  REM 若重名，附加 _ID 避免覆蓋
  if exist "!OUT!" set "OUT=%%B_%%A.json"

  echo   - %%A  ^>  !OUT!
  curl.exe -s -b cookies.txt "%BASE%/rest/workflows/%%A" -o "!OUT!"
)


del workflows.json
echo Done. Files are in: %CD%
python convert_workflow.py