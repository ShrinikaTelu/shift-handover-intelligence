# 🔴 Railway Deployment Issue - Root Cause & Solution

## What's Happening?

When Railway connects to your GitHub repo, it's trying to auto-detect the build method using **Railpack**. But it's finding a monorepo (frontend + backend), so it can't determine what to build.

**Error**: "Error creating build plan with Railpack"

**Reason**: Railway doesn't know whether to build Node.js, Python, or both.

---

## ✅ The Real Solution

You need to tell Railway **explicitly which Dockerfile to use for each service**. This is done in the **Railway Web UI**, not in config files.

### Important: You MUST Do This in the Railroad Web Interface!

When you add a service, Railway shows a form like this:

```
Service Name: _________________
GitHub Repo:  [shift-handover-intelligence]

⚙️ Settings
├─ Builder Type: [Auto Detect] ← CHANGE THIS!
├─ Dockerfile: [auto detected] ← AND THIS!
└─ Build Context: .
```

---

## 🎯 EXACT STEPS TO FIX (In Railway UI)

### If You Already Have a Failed Service:

1. Go to: https://railway.app/dashboard
2. Find your project
3. **DELETE the failed service:**
   - Click the service
   - Click "Settings" (gear icon)
   - Scroll to "**Danger Zone**"
   - Click "**Delete Service**"
4. Start fresh with the steps below

---

### DEPLOY BACKEND (Step by Step with Screenshots Instructions)

1. Go to Railway: https://railway.app/dashboard
2. Create New Project → Click "Create"
3. Click "**+ New**"
4. Click "**Service**"
5. Click "**GitHub Repo**"
6. **Search for your repo:**
   - Type: `shift-handover-intelligence`
   - Click to select it

**Now you're in the service creation screen. IMPORTANT:**

7. Look at the right side panel. You should see:
   - Service Name field
   - Some auto-detected settings

8. **Click somewhere to access settings** (look for "Settings", "Config", or a gear icon)

9. **Find the "Builder" or "Build Method" setting:**
   - Default might show: "Railpack" or "Auto"
   - **Change it to: "Docker"** or **"Dockerfile"**

10. **Find the "Dockerfile" field:**
    - It might say "auto detected" or be empty
    - **Change it to: `Dockerfile.backend`**

11. **Check "Build Context":**
    - Should be: `.` (current/root directory)

12. **Click "Deploy"**

⏳ **Wait 5-10 minutes for build to complete**

---

### ADD ENVIRONMENT VARIABLES

Once backend shows "Deployment Successful":

1. Click on the **backend service**
2. Look for **"Environment"** or **"Variables"** tab
3. Click **"New Variable"** or **"+ Add"**
4. Add these one by one:

| Key | Value |
|-----|-------|
| GEMINI_API_KEY | your_actual_api_key_here |
| DATABASE_URL | sqlite+aiosqlite:///./handover.db |
| ALLOWED_ORIGINS | * |
| DEBUG | false |
| LOG_LEVEL | INFO |

5. **Save/Apply variables**
6. **Restart the service** (should be a button nearby)

⏳ **Wait for restart (1-2 minutes)**

---

### DEPLOY FRONTEND (Same Steps)

1. In the **same Railway project**, click **"+ New"**
2. Click **"Service"**
3. Click **"GitHub Repo"**
4. Select: `shift-handover-intelligence` again

5. **In the settings:**
   - Builder: **"Docker"**
   - Dockerfile: **`Dockerfile.frontend`**
   - Build Context: `.`

6. Click **"Deploy"**

⏳ **Wait 5-10 minutes for build to complete**

---

### GET YOUR LIVE URLs

Once BOTH services show "Deployment Successful":

1. **Backend URL:**
   - Click backend service
   - Top right should show "View" button or the public URL
   - Copy it (looks like: `https://shift-handover-backend-prod.railway.app`)

2. **Frontend URL:**
   - Click frontend service  
   - Top right should show "View" button or the public URL
   - Copy it (looks like: `https://shift-handover-frontend-prod.railway.app`)

---

### CONNECT FRONTEND TO BACKEND

The frontend doesn't know where the backend is. You need to tell it:

1. **Open in your code editor:**
   ```
   frontend/src/app/services/handover.service.ts
   ```

2. **Find line ~12:**
   ```typescript
   private readonly API_URL = 'http://localhost:8000/api';
   ```

3. **Replace with your backend URL:**
   ```typescript
   private readonly API_URL = 'https://shift-handover-backend-prod.railway.app/api';
   ```
   (Use YOUR actual backend URL from step above)

4. **Save**

5. **Commit and push:**
   ```bash
   cd /Users/shrinikatelu/shift-handover-project
   git add frontend/src/app/services/handover.service.ts
   git commit -m "Update API URL for Railway deployment"
   git push origin main
   ```

6. **Railway will auto-rebuild frontend** (2-3 minutes)

---

## ✅ Test It!

Once everything is deployed:

1. Open your **frontend URL** in browser:
   ```
   https://shift-handover-frontend-prod.railway.app
   ```

2. You should see the form ✅
3. Try uploading a file ✅
4. Try entering notes ✅
5. Click "Generate Handover" ✅

If it works → **Your app is LIVE!** 🎉

---

## If It Still Fails

### Check What the Error Is:

1. Click on the service that failed
2. Look for **"Logs"** or **"Build Logs"** tab
3. **Scroll through and find the actual error message**
4. Common errors:

**"Cannot find package.json"**
→ Means it's not finding the frontend folder
→ Make sure Dockerfile is set to `Dockerfile.frontend`

**"No such file or directory: requirements.txt"**
→ Means it's not finding the backend folder  
→ Make sure Dockerfile is set to `Dockerfile.backend`

**"Build context not found"**
→ Build context should be `.` (root directory)

**"Port 8000 already in use"**
→ Service might have restarted
→ Click "Restart" button

### If You Can't Figure It Out:

1. Delete the service
2. Try again from scratch
3. Double-check the Dockerfile name matches EXACTLY
4. Make sure Build Context is `.`

---

## Summary

**The KEY is in Railway's UI settings:**

For Backend Service:
```
Builder: Docker
Dockerfile: Dockerfile.backend
Build Context: .
```

For Frontend Service:
```
Builder: Docker
Dockerfile: Dockerfile.frontend
Build Context: .
```

If you set these correctly, the build will work! 💯

---

## Files That Were Already Created

These files are in your repo to help Railway:
- ✅ `docker-compose.yml` - For local Docker testing
- ✅ `Dockerfile.backend` - Backend build instructions
- ✅ `Dockerfile.frontend` - Frontend build instructions
- ✅ `railway.toml` - Railway config (monorepo support)
- ✅ `.dockerignore` - Files to ignore in Docker builds

**You don't need to change any of these.** Just use the correct settings in Railway's UI!

Good luck! 🚀
