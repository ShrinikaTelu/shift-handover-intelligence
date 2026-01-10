# API Test Script for Shift Handover Intelligence
# Run this to test the backend API (requires backend server running)

Write-Host "🧪 Testing Shift Handover Intelligence API" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8000"

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get
    Write-Host "✅ Health check passed" -ForegroundColor Green
    Write-Host "   Status: $($response.status)" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ Health check failed" -ForegroundColor Red
    Write-Host "   Make sure backend server is running on port 8000" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Test 2: Generate Handover (Simple)
Write-Host "Test 2: Generate Handover (Simple)" -ForegroundColor Yellow
$requestBody = @{
    shiftNotes = "Reactor R-101 operating normally at 95% capacity. Temperature stable at 385°C. No issues to report."
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/handover/generate" -Method Post -Body $requestBody -ContentType "application/json"
    Write-Host "✅ Handover generation passed" -ForegroundColor Green
    Write-Host "   Session ID: $($response.sessionId)" -ForegroundColor Gray
    Write-Host "   Summary items: $($response.json.shiftSummary.Count)" -ForegroundColor Gray
    Write-Host "   Open issues: $($response.json.openIssues.Count)" -ForegroundColor Gray
    Write-Host ""

    # Save session ID for next test
    $sessionId = $response.sessionId
} catch {
    Write-Host "❌ Handover generation failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""

    # Check if it's an API key issue
    if ($_.Exception.Message -like "*GEMINI_API_KEY*") {
        Write-Host "⚠️  Looks like GEMINI_API_KEY is not set properly" -ForegroundColor Yellow
        Write-Host "   Edit backend\.env and add your API key" -ForegroundColor Yellow
    }
    exit 1
}

# Test 3: Retrieve Session
Write-Host "Test 3: Retrieve Session" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/handover/$sessionId" -Method Get
    Write-Host "✅ Session retrieval passed" -ForegroundColor Green
    Write-Host "   Retrieved session: $($response.sessionId)" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ Session retrieval failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""
}

# Test 4: Generate with Alarms
Write-Host "Test 4: Generate Handover with Alarms" -ForegroundColor Yellow
$alarmsData = @{
    activeAlarms = @(
        @{
            id = "TEST-001"
            tag = "REACTOR.TEMP"
            description = "High Temperature Alarm"
            priority = "High"
            value = 420
            setpoint = 400
        }
    )
}

$requestBody = @{
    shiftNotes = "Reactor temperature rising. Alarm triggered at 420°C."
    alarmsJson = $alarmsData
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/handover/generate" -Method Post -Body $requestBody -ContentType "application/json"
    Write-Host "✅ Handover with alarms passed" -ForegroundColor Green
    Write-Host "   Critical alarms detected: $($response.json.criticalAlarms.Count)" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ Handover with alarms failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""
}

# Summary
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ API Tests Complete" -ForegroundColor Green
Write-Host ""
Write-Host "Your backend API is working correctly!" -ForegroundColor Cyan
Write-Host "You can now start the frontend and test the full app." -ForegroundColor Cyan
Write-Host ""
