# Backend Quick Start
# Run from the backend/ folder

Write-Host "🚀 Starting Shift Handover Intelligence Backend" -ForegroundColor Cyan

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found. Run setup first:" -ForegroundColor Red
    Write-Host "   python -m venv venv" -ForegroundColor Yellow
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found" -ForegroundColor Yellow
    Write-Host "Creating from template..." -ForegroundColor Gray
    Copy-Item .env.example .env
    Write-Host "Please edit .env and add your GEMINI_API_KEY" -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python main.py
