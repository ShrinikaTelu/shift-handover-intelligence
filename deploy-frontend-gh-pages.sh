#!/bin/bash

# Shift Handover Intelligence - GitHub Pages Deployment Script
# This script deploys the Angular frontend to GitHub Pages

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Shift Handover Intelligence${NC}"
echo -e "${BLUE}GitHub Pages Deployment${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Step 1: Get the Railway Backend URL
echo -e "${BLUE}Step 1: Configure Backend API URL${NC}"
read -p "Enter your Railway Backend URL (e.g., https://shift-handover-intelligence-production.up.railway.app): " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
  echo -e "${RED}❌ Backend URL cannot be empty!${NC}"
  exit 1
fi

# Remove trailing slash if present
BACKEND_URL="${BACKEND_URL%/}"

echo -e "${GREEN}✅ Backend URL configured: $BACKEND_URL${NC}"
echo ""

# Step 2: Update the service with the correct API URL
echo -e "${BLUE}Step 2: Updating API URL in service...${NC}"

cd "$(dirname "$0")/frontend"

# Update the handover.service.ts with the correct API URL
sed -i '' "s|http://localhost:8000/api|$BACKEND_URL/api|g" src/app/services/handover.service.ts
sed -i '' "s|http://localhost:8000/health|$BACKEND_URL/health|g" src/app/services/handover.service.ts

echo -e "${GREEN}✅ API URL updated${NC}"
echo ""

# Step 3: Install dependencies
echo -e "${BLUE}Step 3: Installing dependencies...${NC}"
npm install
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Step 4: Build the project
echo -e "${BLUE}Step 4: Building Angular project...${NC}"
npm run build -- --configuration production --base-href=/shift-handover-intelligence/
echo -e "${GREEN}✅ Build complete${NC}"
echo ""

# Step 5: Deploy to GitHub Pages
echo -e "${BLUE}Step 5: Deploying to GitHub Pages...${NC}"

# Check if ngh is installed, if not install it
if ! command -v ngh &> /dev/null; then
  echo "Installing angular-cli-ghpages..."
  npm install -g angular-cli-ghpages
fi

ngh --dir=dist/frontend/browser --repo=https://github.com/ShrinikaTelu/shift-handover-intelligence.git --branch=gh-pages --message="Deploy: $(date)"

echo -e "${GREEN}✅ Frontend deployed to GitHub Pages!${NC}"
echo ""

# Step 6: Display the live URL
echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo -e "${GREEN}Frontend URL: https://ShrinikaTelu.github.io/shift-handover-intelligence/${NC}"
echo -e "${GREEN}Backend URL: $BACKEND_URL${NC}"
echo -e "${GREEN}API Docs: $BACKEND_URL/docs${NC}"
echo ""
echo -e "${YELLOW}Note: GitHub Pages may take 1-2 minutes to update${NC}"
echo ""
