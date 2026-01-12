# 🚀 Quick Start: Deploy to Railway - UPDATED

## ⚠️ Important: Manual Service Setup Required

Because this is a monorepo (frontend + backend in one repo), you need to manually create each service in Railway.

## Step 1: Sign Up on Railway
👉 Go to **https://railway.app** and sign up with GitHub

## Step 2: Create Backend Service First

1. Go to Railway Dashboard: https://railway.app/dashboard
2. Click "**Create New Project**"
3. Click "**Create**" (empty project)
4. Click "**+ New**" button → "**Service**" → "**GitHub Repo**"
5. Connect your `shift-handover-intelligence` repository
6. In the right panel, configure:
   - **Root Directory**: `backend`
   - **Dockerfile**: `../Dockerfile.backend`
   - Click "Deploy"

## Step 3: Configure Backend Environment Variables

Click on the backend service → "**Variables**" tab

Add these variables:
```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./handover.db
ALLOWED_ORIGINS=*
DEBUG=false
LOG_LEVEL=INFO
```

**⚠️ Replace** `your_gemini_api_key_here` with your actual Gemini API key from Google AI Studio

## Step 4: Create Frontend Service

1. In the same Railway project, click "**+ New**"
2. Click "**Service**" → "**GitHub Repo**"
3. Select `shift-handover-intelligence` again
4. In the right panel:
   - **Root Directory**: `frontend`
   - **Dockerfile**: `../Dockerfile.frontend`
   - Click "Deploy"

## Step 5: Wait for Both Services to Deploy

Each service will:
1. Install dependencies
2. Build the application
3. Start the server

**Expected time**: 10-15 minutes total

Check logs in Railway to see build progress.

## Step 6: Get Your Service URLs

Once both services are deployed:

### Backend URL:
1. Click on backend service
2. Click "**View**" or find the domain in settings
3. Copy the URL (e.g., `https://backend-prod.railway.app`)

### Frontend URL:
1. Click on frontend service  
2. Click "**View**" or find the domain in settings
3. Copy the URL (e.g., `https://frontend-prod.railway.app`)

## Step 7: Connect Frontend to Backend

1. Open `frontend/src/app/services/handover.service.ts`
2. Find this line (around line 12):
   ```typescript
   private readonly API_URL = 'http://localhost:8000/api';
   ```
3. Replace with your backend URL:
   ```typescript
   private readonly API_URL = 'https://your-backend-url.railway.app/api';
   ```
4. Save and commit:
   ```bash
   cd /Users/shrinikatelu/shift-handover-project
   git add frontend/src/app/services/handover.service.ts
   git commit -m "Update API URL for Railway deployment"
   git push origin main
   ```

Railway will automatically redeploy the frontend with the new API URL!

## Step 8: Your App is Live! 🎉

Access your application:
```
https://your-frontend-url.railway.app
```

---

## Troubleshooting

### ❌ Deployment fails with Nixpacks error
- **Solution**: Make sure you selected the correct Dockerfile path
- Check: Root Directory should be `frontend` or `backend`, not root

### ❌ Frontend shows blank page
- Check browser console (F12) for errors
- Verify API URL in `handover.service.ts` matches your backend URL
- Check CORS settings in backend

### ❌ API calls fail (Error 404 or 503)
1. Go to Railway → backend service
2. Click "**View**" to check if it's actually running
3. Check logs for errors
4. Verify all environment variables are set correctly

### ❌ Build fails
1. Click on the service
2. Go to "**Logs**" tab to see error messages
3. Common issues:
   - Missing dependencies in `package.json` or `requirements.txt`
   - Wrong Dockerfile path
   - Port conflicts

### 🟡 Deployment takes too long
- First deployment is slower (installing all dependencies)
- Subsequent deployments are faster (caching)
- Maximum timeout is ~30 minutes

---

## Next Steps (Optional)

- **Custom Domain**: Railway Settings → Custom Domains
- **Environment**: Add more environment variables per service
- **Monitoring**: Enable logs and alerts
- **Database**: Add PostgreSQL from Railway plugins (if needed)

---

## Service Architecture

```
Your GitHub Repository (shift-handover-intelligence)
        ↓
    Railway Project
        ├── Backend Service (Python/FastAPI)
        │   └── Deployed from: backend/ folder
        │   └── URL: https://backend-xxx.railway.app
        │
        └── Frontend Service (Node.js/Angular)
            └── Deployed from: frontend/ folder
            └── URL: https://frontend-xxx.railway.app
```

---

## Important Notes

1. **Each service runs independently** on Railway
2. **Automatic updates**: Push to `main` → Railway auto-deploys
3. **Environment variables**: Keep API keys safe in Railway settings
4. **Logs**: Always check Railway logs if something isn't working
5. **Free tier limits**: Railway offers good free tier but monitor usage

Good luck! 🚀

