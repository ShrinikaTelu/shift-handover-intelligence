#!/bin/bash#!/bin/bash

# Shift Handover Intelligence - Full Stack Deployment Script# Shift Handover Intelligence - Full Stack Deployment Script



set -eset -e



# Colors for output# Colors for output

GREEN='\033[0;32m'GREEN='\033[0;32m'

BLUE='\033[0;34m'BLUE='\033[0;34m'

YELLOW='\033[1;33m'YELLOW='\033[1;33m'

RED='\033[0;31m'RED='\033[0;31m'

NC='\033[0m'NC='\033[0m'



echo -e "${BLUE}================================${NC}"echo -e "${BLUE}================================${NC}"

echo -e "${BLUE}Shift Handover Intelligence${NC}"echo -e "${BLUE}Shift Handover Intelligence${NC}"

echo -e "${BLUE}Full Stack Deployment Script${NC}"echo -e "${BLUE}Full Stack Deployment Script${NC}"

echo -e "${BLUE}================================${NC}"echo -e "${BLUE}================================${NC}"

echo ""echo ""



# Step 1: Get the Railway API URL# Step 1: Get the Railway API URL

echo -e "${BLUE}Step 1: Configure Railway Backend URL${NC}"echo -e "${BLUE}Step 1: Configure Railway Backend URL${NC}"

read -p "Enter your Railway API URL (e.g., https://shift-handover-backend-abc.up.railway.app): " RAILWAY_URLread -p "Enter your Railway API URL (e.g., https://shift-handover-backend-abc.up.railway.app): " RAILWAY_URL



if [ -z "$RAILWAY_URL" ]; thenif [ -z "$RAILWAY_URL" ]; then

  echo -e "${RED}❌ Railway URL cannot be empty!${NC}"  echo -e "${RED}❌ Railway URL cannot be empty!${NC}"

  exit 1  exit 1

fifi



echo -e "${GREEN}✓ Using Railway API: $RAILWAY_URL${NC}"echo -e "${GREEN}✓ Using Railway API: $RAILWAY_URL${NC}"

echo ""echo ""



# Step 2: Update frontend API endpoint# Step 2: Update frontend API endpoint

echo -e "${BLUE}Step 2: Updating frontend API endpoint...${NC}"echo -e "${BLUE}Step 2: Updating frontend API endpoint...${NC}"



FRONTEND_SERVICE="./frontend/src/app/services/handover.service.ts"FRONTEND_SERVICE="./frontend/src/app/services/handover.service.ts"



if [ -f "$FRONTEND_SERVICE" ]; thenif [ -f "$FRONTEND_SERVICE" ]; then

  # Replace the localhost API URL with the Railway URL  # Replace the localhost API URL with the Railway URL

  sed -i '' "s|http://localhost:8000|$RAILWAY_URL|g" "$FRONTEND_SERVICE"  sed -i '' "s|http://localhost:8000|$RAILWAY_URL|g" "$FRONTEND_SERVICE"

  echo -e "${GREEN}✓ Frontend API endpoint updated${NC}"  echo -e "${GREEN}✓ Frontend API endpoint updated${NC}"

elseelse

  echo -e "${RED}⚠️  Could not find handover.service.ts${NC}"  echo -e "${RED}⚠️  Could not find handover.service.ts${NC}"

fifi

echo ""echo ""



# Step 3: Build frontend for production# Step 3: Build frontend for production

echo -e "${BLUE}Step 3: Building frontend for production...${NC}"echo -e "${BLUE}Step 3: Building frontend for production...${NC}"



cd frontendcd frontend



npm installnpm install

ng build --configuration production --base-href "/shift-handover-intelligence/"ng build --configuration production --base-href "/shift-handover-intelligence/"



echo -e "${GREEN}✓ Frontend built successfully${NC}"echo -e "${GREEN}✓ Frontend built successfully${NC}"

echo ""echo ""



# Step 4: Deploy to GitHub Pages# Step 4: Deploy to GitHub Pages

echo -e "${BLUE}Step 4: Deploying frontend to GitHub Pages...${NC}"echo -e "${BLUE}Step 4: Deploying frontend to GitHub Pages...${NC}"



npx angular-cli-ghpages --dir=dist/shift-handover-intelligence --repo=https://github.com/ShrinikaTelu/shift-handover-intelligence.gitnpx angular-cli-ghpages --dir=dist/shift-handover-intelligence --repo=https://github.com/ShrinikaTelu/shift-handover-intelligence.git



echo -e "${GREEN}✓ Deployed to GitHub Pages!${NC}"echo -e "${GREEN}✓ Deployed to GitHub Pages!${NC}"

echo ""echo ""



# Step 5: Display results# Step 5: Display results

echo -e "${BLUE}================================${NC}"echo -e "${BLUE}================================${NC}"

echo -e "${BLUE}=== Deployment Complete ===${NC}"echo -e "${BLUE}=== Deployment Complete ===${NC}"

echo -e "${BLUE}================================${NC}"echo -e "${BLUE}================================${NC}"

echo ""echo ""

echo -e "${GREEN}✓ Frontend (GitHub Pages):${NC}"echo -e "${GREEN}✓ Frontend (GitHub Pages):${NC}"

echo -e "   https://ShrinikaTelu.github.io/shift-handover-intelligence/"echo -e "   https://ShrinikaTelu.github.io/shift-handover-intelligence/"

echo ""echo ""

echo -e "${GREEN}✓ Backend API (Railway):${NC}"echo -e "${GREEN}✓ Backend API (Railway):${NC}"

echo -e "   $RAILWAY_URL"echo -e "   $RAILWAY_URL"

echo ""echo ""

echo -e "${YELLOW}Next steps:${NC}"echo -e "${YELLOW}Next steps:${NC}"

echo "1. Verify frontend deployment: https://ShrinikaTelu.github.io/shift-handover-intelligence/"echo "1. Verify frontend deployment: https://ShrinikaTelu.github.io/shift-handover-intelligence/"

echo "2. Verify backend is running on Railway"echo "2. Verify backend is running on Railway"

echo "3. Test API endpoints at: $RAILWAY_URL/docs"echo "3. Test API endpoints at: $RAILWAY_URL/docs"

echo ""echo ""

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
