# ✅ Railway Deployment - FINAL FIX

## Problem You're Having:
"Error creating build plan with Railpack"

## Solution:
Railway is trying to auto-detect the language. We need to **explicitly tell it to use Docker**.

---

## 🎯 STEP-BY-STEP INSTRUCTIONS

### IMPORTANT: Delete Failed Deployment First

Before redeploying:
1. Go to https://railway.app/dashboard
2. Find your project
3. Click on the service that failed
4. Click "Settings" (gear icon)
5. Scroll down → "Danger Zone" → Click "Delete Service"
6. Repeat for all failed services

---

### DEPLOY BACKEND SERVICE

1. Go to: https://railway.app/dashboard
2. Click "Create New Project"
3. Click "Create" (blank project)
4. Click the "+ New" button
5. Select "**Service**" → "**GitHub Repo**"
6. Search for and select: `shift-handover-intelligence`

Now you'll see the repo connected. Look for the **right sidebar**:

7. **Click on "Settings"** (should be a gear icon or at top of right panel)
8. Look for **"Builder"** setting:
   - Select: **"Docker"**
   
9. Look for **"Dockerfile Path"**:
   - Enter: `Dockerfile.backend`
   
10. Click **"Deploy"**

**Wait for it to build** (5-10 minutes)

---

### ADD ENVIRONMENT VARIABLES TO BACKEND

Once backend deployment finishes:

1. Click on the **backend service** in the project
2. Go to **"Variables"** tab (or "Environment" tab)
3. Click "**New Variable**"
4. Add each of these:

```
GEMINI_API_KEY = your_actual_api_key_here
DATABASE_URL = sqlite+aiosqlite:///./handover.db
ALLOWED_ORIGINS = *
DEBUG = false
LOG_LEVEL = INFO
```

4. After adding all variables, click the **"Restart"** button to apply them

---

### DEPLOY FRONTEND SERVICE

1. In the **same Railway project**, click "**+ New**"
2. Select "**Service**" → "**GitHub Repo**"
3. Search for and select: `shift-handover-intelligence` again
4. In the right sidebar:

5. **Click on "Settings"**
6. Look for **"Builder"**:
   - Select: **"Docker"**
   
7. Look for **"Dockerfile Path"**:
   - Enter: `Dockerfile.frontend`
   
8. Click **"Deploy"**

**Wait for it to build** (5-10 minutes)

---

### GET YOUR URLS

Once both services show "**Deployment Successful**":

**Backend URL:**
1. Click on backend service
2. Look at the top or right panel for "**View**" button or domain name
3. It will look like: `https://shift-handover-backend-prod.railway.app`
4. **Copy this URL**

**Frontend URL:**
1. Click on frontend service
2. Look at the top or right panel for "**View**" button or domain name
3. It will look like: `https://shift-handover-frontend-prod.railway.app`
4. **Copy this URL**

---

### CONNECT FRONTEND TO BACKEND

1. **Open this file in your code editor:**
   ```
   frontend/src/app/services/handover.service.ts
   ```

2. **Find this line** (around line 12):
   ```typescript
   private readonly API_URL = 'http://localhost:8000/api';
   ```

3. **Replace it with** (use YOUR actual backend URL):
   ```typescript
   private readonly API_URL = 'https://shift-handover-backend-prod.railway.app/api';
   ```

4. **Save the file**

5. **Push to GitHub:**
   ```bash
   cd /Users/shrinikatelu/shift-handover-project
   git add frontend/src/app/services/handover.service.ts
   git commit -m "Update API URL for Railway deployment"
   git push origin main
   ```

6. **Railway will automatically rebuild frontend** (2-3 minutes)

---

### VERIFY IT WORKS

1. Open your frontend URL in a browser:
   ```
   https://shift-handover-frontend-prod.railway.app
   ```

2. You should see the Shift Handover form

3. Try uploading a file or entering notes

4. **If it works** → Your app is live! 🎉

---

## If It Still Fails

### Check Build Logs:

1. Click on the service that failed
2. Look for "**Logs**" tab (or similar)
3. **Scroll through the logs** to find the error
4. Common errors:
   - **"npm not found"** → package.json might be missing
   - **"pip not found"** → requirements.txt might be missing
   - **"port already in use"** → Restart the service

### If Logs Show Error in Dockerfile:

1. You might need to rebuild from scratch:
   - Delete the service
   - Redeploy from scratch (follow steps above)

### Ask for Help:

Go to Railway Discord: https://discord.gg/railway

Copy the full error from the logs and paste it there.

---

## Summary

**What Railway will do:**
1. ✅ Pull your code from GitHub
2. ✅ Read `Dockerfile.backend` (for backend service)
3. ✅ Build a Docker image for the backend
4. ✅ Run the backend on port 8000
5. ✅ Read `Dockerfile.frontend` (for frontend service)
6. ✅ Build a Docker image for the frontend
7. ✅ Run the frontend on port 80 (Nginx)
8. ✅ Assign URLs to both services
9. ✅ Your app is live!

You're almost there! 🚀
