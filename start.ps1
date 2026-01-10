# Shift Handover Intelligence - Quick Start Script
# Run this from the shift-handover-intelligence folder

Write-Host "🏭 Shift Handover Intelligence - Setup & Start" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "❌ Error: Please run this script from the shift-handover-intelligence folder" -ForegroundColor Red
    exit 1
}

# Backend Setup
Write-Host "📦 Setting up Backend..." -ForegroundColor Yellow
cd backend

if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Gray
    python -m venv venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Gray
& .\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Gray
pip install -q -r requirements.txt

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found" -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "Created .env from template. Please edit it and add your GEMINI_API_KEY" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press Enter after you've added your Gemini API key to backend\.env" -ForegroundColor Cyan
    Read-Host
}

# Start Backend in background
Write-Host "🚀 Starting Backend Server (http://localhost:8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python main.py"

cd ..

# Frontend Setup
Write-Host ""
Write-Host "📦 Setting up Frontend..." -ForegroundColor Yellow
cd frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node dependencies (this may take a while)..." -ForegroundColor Gray
    npm install
}

# Start Frontend
Write-Host "🚀 Starting Frontend Server (http://localhost:4200)..." -ForegroundColor Green
Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:4200" -ForegroundColor Cyan
Write-Host "Health:   http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the frontend server" -ForegroundColor Yellow
Write-Host ""

ng serve --open
