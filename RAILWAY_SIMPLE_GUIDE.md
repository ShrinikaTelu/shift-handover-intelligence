# 🚀 Deploy to Railway - Simple Instructions

## What You Need to Know

This project has **TWO services**:
- **Frontend** (Angular) - Served by Nginx
- **Backend** (Python FastAPI) - REST API

Both are already configured with Dockerfiles. Railway will use them automatically.

---

## Step 1: Create First Service (Backend)

1. Go to **https://railway.app/dashboard**
2. Click **"Create New Project"**
3. Click **"Create"** (empty project)
4. Click **"+ New Service"**
5. Select **"GitHub Repo"**
6. Search and select: **`shift-handover-intelligence`**
7. Click **"Deploy"**

---

## Step 2: Configure Backend Service

Railway will auto-detect the Dockerfile. If it asks:
- **Dockerfile**: Leave as default or select `Dockerfile.backend`
- Click **"Deploy"**

Wait for build to complete...

---

## Step 3: Add Backend Environment Variables

Once backend is deployed:

1. Click on the **backend service**
2. Go to **"Variables"** tab
3. Add these variables:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   DATABASE_URL=sqlite+aiosqlite:///./handover.db
   ALLOWED_ORIGINS=*
   DEBUG=false
   LOG_LEVEL=INFO
   ```

4. **Restart the service** after adding variables

---

## Step 4: Create Second Service (Frontend)

1. In the **same Railway project**, click **"+ New Service"**
2. Select **"GitHub Repo"**
3. Select: **`shift-handover-intelligence`** again
4. If asked which Dockerfile:
   - Select **`Dockerfile.frontend`**
5. Click **"Deploy"**

Wait for build to complete...

---

## Step 5: Get Your URLs

Once both services are deployed:

### Backend URL:
1. Click on **backend service**
2. In the right panel, look for **"Public URL"** or **"Domain"**
3. Copy it (e.g., `https://shift-handover-backend-prod.railway.app`)

### Frontend URL:
1. Click on **frontend service**
2. In the right panel, look for **"Public URL"** or **"Domain"**
3. Copy it (e.g., `https://shift-handover-frontend-prod.railway.app`)

---

## Step 6: Connect Frontend to Backend

⚠️ **IMPORTANT**: The frontend needs to know where the backend is.

1. Open this file in your editor:
   ```
   frontend/src/app/services/handover.service.ts
   ```

2. Find line ~12:
   ```typescript
   private readonly API_URL = 'http://localhost:8000/api';
   ```

3. Replace with your actual backend URL:
   ```typescript
   private readonly API_URL = 'https://shift-handover-backend-prod.railway.app/api';
   ```
   (Use your actual backend URL from Step 5)

4. Save the file

5. Commit and push:
   ```bash
   git add frontend/src/app/services/handover.service.ts
   git commit -m "Update backend API URL for Railway"
   git push origin main
   ```

6. **Railway will automatically rebuild and redeploy** the frontend

---

## Step 7: Your App is Live! 🎉

Visit your frontend URL in a browser:
```
https://shift-handover-frontend-prod.railway.app
```

(Replace with your actual frontend URL)

---

## Troubleshooting

### ❌ Backend build fails
→ Check logs in Railway dashboard
→ Make sure `requirements.txt` is in the `backend/` folder
→ Verify Python version compatibility

### ❌ Frontend build fails
→ Check logs in Railway dashboard
→ Make sure `package.json` is in the `frontend/` folder
→ Verify Node.js version compatibility

### ❌ Frontend loads but API calls fail
→ Check browser console (F12 → Console tab)
→ Verify API URL is correct in `handover.service.ts`
→ Check backend is actually running in Railway
→ Verify `ALLOWED_ORIGINS` in backend includes your frontend URL

### ❌ "Build failed - Nixpacks error"
→ This means Railway is trying to auto-detect the language
→ **Solution**: Make sure you're selecting the correct Dockerfile when deploying

---

## What Happens Next?

- Every time you push to GitHub, Railway automatically rebuilds and redeploys
- Your app will be live at the URLs from Step 5
- Share the frontend URL with users!

---

## Need Help?

- Railway Docs: https://docs.railway.app
- Check service logs in Railway dashboard
- Verify environment variables are set correctly
- Make sure both services are in "Success" status

Good luck! 🚀
