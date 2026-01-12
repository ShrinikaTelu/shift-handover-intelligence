#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

REPO_OWNER="ShrinikaTelu"
REPO_NAME="shift-handover-intelligence"
FRONTEND_DIR="frontend"
ENV_DIR="$FRONTEND_DIR/src/environments"
ENV_FILE="$ENV_DIR/environment.ts"
ENV_DEV_FILE="$ENV_DIR/environment.development.ts"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Shift Handover Intelligence${NC}"
echo -e "${BLUE}Frontend Deployment to GitHub Pages${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Step 1: Get the Railway API URL
echo -e "${BLUE}Step 1: Configure Railway Backend URL${NC}"
read -p "Enter your Railway Backend URL (e.g., https://shift-handover-intelligence-production.up.railway.app): " RAILWAY_URL

if [ -z "$RAILWAY_URL" ]; then
  echo -e "${RED}❌ Railway URL cannot be empty!${NC}"
  exit 1
fi

# Normalize URL (remove trailing slash)
RAILWAY_URL=${RAILWAY_URL%/}

API_URL="$RAILWAY_URL/api"
HEALTH_URL="$RAILWAY_URL/health"

echo -e "${GREEN}✓ Using Backend API: $API_URL${NC}"
echo -e "${GREEN}✓ Using Health URL: $HEALTH_URL${NC}"
echo ""

# Step 2: Write Angular environment files
echo -e "${BLUE}Step 2: Preparing Angular environment files...${NC}"
mkdir -p "$ENV_DIR"

cat > "$ENV_FILE" <<EOF
export const environment = {
  production: true,
  apiUrl: '$API_URL',
  healthUrl: '$HEALTH_URL'
};
EOF

cat > "$ENV_DEV_FILE" <<EOF
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  healthUrl: 'http://localhost:8000/health'
};
EOF

echo -e "${GREEN}✓ environment.ts and environment.development.ts updated${NC}"
echo ""

# Step 3: Install deps and build frontend
echo -e "${BLUE}Step 3: Building frontend for production...${NC}"
pushd "$FRONTEND_DIR" >/dev/null

# Prefer clean, reproducible install
if command -v npm >/dev/null 2>&1; then
  npm ci || npm install
else
  echo -e "${RED}❌ npm not found. Please install Node.js and npm.${NC}"
  exit 1
fi

# Use npx to avoid requiring global Angular CLI
npx ng build --configuration production --base-href "/$REPO_NAME/"

echo -e "${GREEN}✓ Frontend built successfully${NC}"
echo ""

# Step 4: Deploy to GitHub Pages
echo -e "${BLUE}Step 4: Deploying to GitHub Pages...${NC}"
npx angular-cli-ghpages \
  --dir=dist/frontend/browser \
  --repo=https://github.com/$REPO_OWNER/$REPO_NAME.git \
  --no-silent

popd >/dev/null

echo -e "${GREEN}✓ Deployed to GitHub Pages!${NC}"
echo ""

# Step 5: Display results
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}=== Deployment Complete ===${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}✓ Frontend (GitHub Pages):${NC}"
echo -e "   https://$REPO_OWNER.github.io/$REPO_NAME/"
echo ""
echo -e "${GREEN}✓ Backend API (Railway):${NC}"
echo -e "   $RAILWAY_URL"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Verify frontend: https://$REPO_OWNER.github.io/$REPO_NAME/"
echo "2. Verify backend: $RAILWAY_URL/docs"
echo "3. If CORS issues, ensure backend allows https://$REPO_OWNER.github.io"
