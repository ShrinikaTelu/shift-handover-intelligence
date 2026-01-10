#!/bin/bash

# Shift Handover Intelligence - Quick Deployment Script
# This script helps you deploy the application locally or to cloud

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Shift Handover Intelligence - Deployment Helper"
echo "=================================================="
echo ""

# Check for required tools
check_requirements() {
    echo "📋 Checking prerequisites..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3.9+ not found"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js not found"
        exit 1
    fi
    
    echo "✅ Python: $(python3 --version)"
    echo "✅ Node.js: $(node --version)"
    echo ""
}

# Setup environment
setup_env() {
    echo "🔧 Setting up environment..."
    
    if [ ! -f "$SCRIPT_DIR/.env" ]; then
        if [ -f "$SCRIPT_DIR/.env.example" ]; then
            cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
            echo "✅ Created .env from .env.example"
            echo "⚠️  IMPORTANT: Update .env with your GOOGLE_API_KEY"
            read -p "Press Enter after updating .env..."
        else
            echo "❌ .env.example not found"
            exit 1
        fi
    else
        echo "✅ .env already exists"
    fi
}

# Install backend dependencies
install_backend() {
    echo ""
    echo "🔧 Installing backend dependencies..."
    cd "$SCRIPT_DIR/backend"
    
    if python3 -m pip install -r requirements.txt; then
        echo "✅ Backend dependencies installed"
    else
        echo "❌ Failed to install backend dependencies"
        exit 1
    fi
    
    cd "$SCRIPT_DIR"
}

# Install frontend dependencies
install_frontend() {
    echo ""
    echo "🔧 Installing frontend dependencies..."
    cd "$SCRIPT_DIR/frontend"
    
    if npm install; then
        echo "✅ Frontend dependencies installed"
    else
        echo "❌ Failed to install frontend dependencies"
        exit 1
    fi
    
    cd "$SCRIPT_DIR"
}

# Start backend
start_backend() {
    echo ""
    echo "🚀 Starting backend server (port 8000)..."
    cd "$SCRIPT_DIR/backend"
    
    export PYTHONPATH="$SCRIPT_DIR/backend"
    python3 << 'EOF' &
from main import app
import uvicorn
uvicorn.run(app, host='127.0.0.1', port=8000)
EOF
    
    echo "✅ Backend started (PID: $!)"
    sleep 3
    cd "$SCRIPT_DIR"
}

# Start frontend
start_frontend() {
    echo ""
    echo "🚀 Starting frontend server (port 4200)..."
    cd "$SCRIPT_DIR/frontend"
    
    npx ng serve --host 0.0.0.0 &
    
    echo "✅ Frontend started"
    sleep 5
    cd "$SCRIPT_DIR"
}

# Main menu
show_menu() {
    echo ""
    echo "Select deployment option:"
    echo "1) Install dependencies"
    echo "2) Start backend only"
    echo "3) Start frontend only"
    echo "4) Start both (full local dev)"
    echo "5) Docker deployment (requires Docker)"
    echo "6) Cloud deployment (Railway.app)"
    echo "7) Exit"
    echo ""
}

# Docker deployment
docker_deploy() {
    echo ""
    echo "🐳 Docker Deployment"
    echo "==================="
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Install from https://docker.com"
        return
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose not found"
        return
    fi
    
    read -p "Build and start containers? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$SCRIPT_DIR"
        docker-compose up -d
        echo "✅ Containers started"
        echo "Backend: http://localhost:8000"
        echo "Frontend: http://localhost:3000"
    fi
}

# Cloud deployment guide
cloud_deploy() {
    echo ""
    echo "☁️  Cloud Deployment Guide"
    echo "=========================="
    echo ""
    echo "Choose your deployment platform:"
    echo ""
    echo "1️⃣  Railway.app (RECOMMENDED)"
    echo "   - Easiest setup for beginners"
    echo "   - Free tier available"
    echo "   - Git auto-deploy"
    echo "   Steps:"
    echo "   a) Create account at railway.app"
    echo "   b) Create new project from GitHub repo"
    echo "   c) Add environment variables"
    echo "   d) Deploy automatically"
    echo ""
    echo "2️⃣  Render.com"
    echo "   - Free tier (with limitations)"
    echo "   - Good documentation"
    echo ""
    echo "3️⃣  Vercel (Frontend) + Railway (Backend)"
    echo "   - Vercel: Deploy frontend"
    echo "   - Railway: Deploy backend API"
    echo ""
    echo "4️⃣  Google Cloud Run"
    echo "   - Native Google integration"
    echo "   - Seamless Gemini API integration"
    echo ""
    
    echo "Visit HACKATHON_DEPLOYMENT.md for detailed setup instructions"
}

# Main script logic
main() {
    check_requirements
    setup_env
    
    while true; do
        show_menu
        read -p "Enter choice (1-7): " choice
        
        case $choice in
            1)
                install_backend
                install_frontend
                echo "✅ All dependencies installed"
                ;;
            2)
                start_backend
                echo ""
                echo "Backend running on http://127.0.0.1:8000"
                echo "API Docs: http://127.0.0.1:8000/docs"
                ;;
            3)
                start_frontend
                echo ""
                echo "Frontend running on http://localhost:4200"
                ;;
            4)
                install_backend
                install_frontend
                start_backend
                start_frontend
                echo ""
                echo "✅ Both servers running!"
                echo "Frontend: http://localhost:4200"
                echo "Backend: http://127.0.0.1:8000"
                echo "API Docs: http://127.0.0.1:8000/docs"
                echo ""
                echo "Press Ctrl+C to stop all servers"
                wait
                ;;
            5)
                docker_deploy
                ;;
            6)
                cloud_deploy
                ;;
            7)
                echo "Goodbye! 👋"
                exit 0
                ;;
            *)
                echo "Invalid choice. Please try again."
                ;;
        esac
    done
}

# Run main script
main
