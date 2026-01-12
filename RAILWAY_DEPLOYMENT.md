# Railway Deployment Guide

This guide will help you deploy the Shift Handover Intelligence application to Railway.

## What is Railway?

Railway is a modern deployment platform that makes it easy to deploy full-stack applications. It supports:
- Node.js (for Angular frontend)
- Python (for FastAPI backend)
- PostgreSQL/SQLite databases
- Environment variables
- Automatic deployments on git push

## Deployment Architecture

```
Your GitHub Repository
        ↓
    Railway
        ├── Frontend (Angular) - Node.js
        └── Backend (FastAPI) - Python
```

## Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub (recommended for easy integration)
3. Connect your GitHub account

## Step 2: Create Railway Project

### Option A: Create from GitHub Repository (Recommended)

1. Go to https://railway.app/dashboard
2. Click "Create New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository: `shift-handover-intelligence`
5. Railway will auto-detect your services

### Option B: Manual Setup

1. Create new project
2. Add services manually:
   - Frontend service
   - Backend service

## Step 3: Configure Services

### Frontend Service (Angular)

1. **Environment Variables:**
   ```
   NODE_ENV=production
   ```

2. **Build Command:**
   ```
   cd frontend && npm install && npm run build
   ```

3. **Start Command:**
   ```
   cd frontend && npx http-server dist/frontend -p $PORT
   ```

   OR use this Procfile approach (see Step 4)

4. **Port:** `3000` (or whatever Railway assigns)

### Backend Service (FastAPI)

1. **Environment Variables:**
   ```
   GEMINI_API_KEY=your_api_key_here
   DATABASE_URL=sqlite+aiosqlite:///./handover.db
   ALLOWED_ORIGINS=https://your-domain.railway.app
   DEBUG=false
   LOG_LEVEL=INFO
   ```

2. **Build Command:**
   ```
   cd backend && pip install -r requirements.txt
   ```

3. **Start Command:**
   ```
   cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Port:** `8000` (or whatever Railway assigns)

## Step 4: Create Procfiles (Optional but Recommended)

### Frontend Procfile

Create `frontend/Procfile`:
```
web: npx http-server dist/frontend -p $PORT
```

### Backend Procfile

Create `backend/Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Step 5: Update Service Connections

After deployment, update your frontend to call the backend API:

**File:** `frontend/src/app/services/handover.service.ts`

```typescript
// Change this line:
// private readonly API_URL = 'http://localhost:8000/api';

// To this (get your Railway backend URL from the dashboard):
private readonly API_URL = 'https://your-backend-domain.railway.app/api';
```

## Step 6: Deploy

### Automatic Deployment (Recommended)

1. Railway watches your GitHub repository
2. Every push to `main` branch triggers automatic deployment
3. No manual steps needed!

### Manual Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Deploy
railway up
```

## Step 7: Get Your Live URLs

After deployment completes:

1. Go to **Railway Dashboard**: https://railway.app/dashboard
2. Click your project
3. Each service will have a unique URL:
   - **Frontend URL**: `https://your-frontend-name.railway.app`
   - **Backend URL**: `https://your-backend-name.railway.app`

Your frontend will be live at something like:
```
https://shift-handover-frontend.railway.app
```

## Step 8: Update API Configuration

Update your handover service with the correct backend URL:

```typescript
// frontend/src/app/services/handover.service.ts
private readonly API_URL = 'https://shift-handover-backend.railway.app/api';
```

Then push to trigger automatic redeployment.

## Important Notes

1. **Environment Variables**: Keep your `GEMINI_API_KEY` safe in Railway's environment variables, never commit it to git
2. **CORS**: Update `ALLOWED_ORIGINS` in backend to include your Railway frontend URL
3. **Database**: The included SQLite database will work, but for production consider using Railway's PostgreSQL add-on
4. **Free Tier**: Railway offers free deployments with reasonable limits

## Troubleshooting

### Frontend builds but doesn't load
- Check that `baseHref` in `angular.json` is set correctly
- Verify the API URL in the service matches your backend

### API calls failing
- Check CORS settings in backend
- Verify `ALLOWED_ORIGINS` includes your frontend URL
- Check backend logs in Railway dashboard

### Build fails
- Check build logs in Railway dashboard
- Ensure all dependencies are in `requirements.txt` and `package.json`
- Verify Node.js and Python versions are compatible

## Next Steps

1. **Sign up on Railway**: https://railway.app
2. **Connect GitHub repository**
3. **Configure environment variables**
4. **Deploy!**
5. **Share your live link**: `https://your-project.railway.app`

## Monitoring

Once deployed, you can:
- View logs in real-time
- Monitor performance
- Set up custom domains
- Configure auto-scaling

---

**Your Live Application Links** (after deployment):
- 🌐 Frontend: `https://shift-handover-frontend.railway.app`
- 🔌 Backend: `https://shift-handover-backend.railway.app`
- 📚 API Docs: `https://shift-handover-backend.railway.app/docs`
