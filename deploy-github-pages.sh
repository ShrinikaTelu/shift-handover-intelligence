#!/bin/bash

# Shift Handover Intelligence - GitHub Pages Deployment Script
# This script deploys the frontend to GitHub Pages with the Railway backend URL

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

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
  echo -e "${RED}❌ Error: frontend directory not found${NC}"
  echo "Please run this script from the project root directory"
  exit 1
fi

# Step 1: Install dependencies
echo -e "${BLUE}Step 1: Installing dependencies...${NC}"
cd frontend
npm install
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 2: Build for production
echo -e "${BLUE}Step 2: Building Angular app for production...${NC}"
npm run build:prod
echo -e "${GREEN}✓ Production build completed${NC}"
echo ""

# Step 3: Deploy to GitHub Pages
echo -e "${BLUE}Step 3: Deploying to GitHub Pages...${NC}"
npm run deploy:gh-pages
echo -e "${GREEN}✓ Deployment complete!${NC}"
echo ""

# Step 4: Display deployment info
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ Deployment Successful!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${BLUE}📱 Frontend URL:${NC}"
echo -e "   https://shrinikatelu.github.io/shift-handover-intelligence/"
echo ""
echo -e "${BLUE}🔌 Backend API:${NC}"
echo -e "   https://shift-handover-intelligence-production.up.railway.app/api"
echo ""
echo -e "${BLUE}📚 API Documentation:${NC}"
echo -e "   https://shift-handover-intelligence-production.up.railway.app/docs"
echo ""
echo -e "${YELLOW}Note: GitHub Pages may take 1-2 minutes to update${NC}"
echo ""
