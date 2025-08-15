@echo off
REM Batch script to launch the Pinecone Query Interface on Windows

echo 🚀 Launching BiWeekly Meeting Notes Q^&A Interface...
echo ============================================================

cd /d "%~dp0"

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  No .env file found!
    echo    Please create .env with your API keys:
    echo    OPENAI_API_KEY=your-openai-key
    echo    PINECONE_API_KEY=your-pinecone-key
    echo.
    pause
)

echo 🌐 Starting Streamlit server...
echo    The interface will open in your web browser
echo    Press Ctrl+C to stop the server
echo.

REM Launch with UV
uv run streamlit run query_interface.py --server.headless=false

pause
