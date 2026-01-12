#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}🚀 Shift Handover Frontend Deploy${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo -e "${RED}❌ Error: package.json not found in frontend directory${NC}"
    echo -e "${RED}Please run this script from the project root directory${NC}"
    exit 1
fi

# Navigate to frontend directory
cd frontend

echo -e "${YELLOW}📦 Installing dependencies...${NC}"
npm install

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}🔨 Building production bundle...${NC}"
npm run build:prod

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to build application${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}📤 Deploying to GitHub Pages...${NC}"
npx ngh --dir=dist/frontend/browser --branch=gh-pages --message="Deploy: $(date '+%Y-%m-%d %H:%M:%S')"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to deploy to GitHub Pages${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}📱 Frontend is now live at:${NC}"
echo -e "${GREEN}https://ShrinikaTelu.github.io/shift-handover-intelligence/${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo -e "${BLUE}Backend API: ${GREEN}https://shift-handover-intelligence-production.up.railway.app${NC}"
echo ""
