# Railway Deployment - Quick Setup Guide

## 🚀 Deploy Backend in 5 Minutes

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Sign Up"
3. Choose "GitHub" and authenticate
4. Authorize Railway to access your GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "GitHub Repo"
3. Choose `shift-handover-intelligence`
4. Click "Deploy"

**Railway will automatically:**
- Detect the `Dockerfile` at root
- Build the Docker image
- Deploy the backend service
- Provide a public URL

### Step 3: Add Environment Variables
1. In Railway dashboard, go to your project
2. Click on the service (should show something like "Dockerfile")
3. Go to **Variables** tab
4. Add these variables:

```
GEMINI_API_KEY=your_api_key_from_https://ai.google.dev
DEBUG=false
DATABASE_URL=sqlite+aiosqlite:///./handover.db
ALLOWED_ORIGINS=*
```

### Step 4: Deploy
1. Click the **Deploy** button
2. Wait for the build to complete (2-3 minutes)
3. You'll see a public URL like:
   ```
   https://shift-handover-backend-xxx.up.railway.app
   ```

**✅ Backend is Live!**

---

## 📱 Deploy Frontend to GitHub Pages

### Step 1: Install Angular CLI
```bash
npm install -g @angular/cli
npm install -g angular-cli-ghpages
```

### Step 2: Get Your Backend URL
Copy the Railway URL from Step 4 above (looks like: `https://shift-handover-backend-xxx.up.railway.app`)

### Step 3: Run Deployment Script
```bash
cd /Users/shrinikatelu/shift-handover-project

chmod +x deploy.sh
./deploy.sh
```

When prompted, paste your Railway URL.

### Step 4: Verify Deployment
The script will give you a GitHub Pages URL:
```
https://ShrinikaTelu.github.io/shift-handover-intelligence/
```

Visit this URL and you should see your application live! 🎉

---

## 🔧 If Deployment Script Fails

Do it manually:

```bash
cd /Users/shrinikatelu/shift-handover-project/frontend

# Update API URL in code
# Edit: src/app/services/handover.service.ts
# Change: private apiUrl = 'http://localhost:8000';
# To: private apiUrl = 'https://shift-handover-backend-xxx.up.railway.app';

# Build
npm install
ng build --configuration production --base-href "/shift-handover-intelligence/"

# Deploy
npx angular-cli-ghpages --dir=dist/shift-handover-intelligence
```

---

## 📊 Your Final URLs

**Frontend (GitHub Pages):**
```
https://ShrinikaTelu.github.io/shift-handover-intelligence/
```

**Backend API (Railway):**
```
https://shift-handover-backend-xxx.up.railway.app
```

**API Documentation:**
```
https://shift-handover-backend-xxx.up.railway.app/docs
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Check GEMINI_API_KEY is set in Railway Variables |
| Frontend shows 404 | Wait 2-3 min for GitHub Pages to deploy |
| API calls fail | Check backend URL in `handover.service.ts` |
| Database error | Ensure `DATABASE_URL` is set (or remove it for SQLite) |

---

## 📝 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Pages                          │
│   https://ShrinikaTelu.github.io/...                   │
│         (Frontend - Angular + Static Files)             │
└────────────────┬──────────────────────────────────────┘
                 │
                 │ API Calls
                 │
┌────────────────▼──────────────────────────────────────┐
│                   Railway.app                          │
│   https://shift-handover-backend-xxx...               │
│    (Backend - FastAPI + Python + SQLite)              │
│    - Handover Processing                              │
│    - Gemini AI Integration                            │
│    - PDF Generation                                   │
└──────────────────────────────────────────────────────┘
```

---

## ✨ What's Next?

1. ✅ Backend running on Railway
2. ✅ Frontend on GitHub Pages
3. 💬 Share the live link with others
4. 📈 Monitor Railway dashboard for stats
5. 🔄 Push updates to `feature/shift-handover-intelligence` branch
6. 🚀 Both services auto-update on each push!

---

## 🔗 Important Links

- Railway Dashboard: https://railway.app/dashboard
- GitHub Pages Settings: https://github.com/ShrinikaTelu/shift-handover-intelligence/settings/pages
- Gemini API Console: https://aistudio.google.com/app/apikey
- Your Live App: https://ShrinikaTelu.github.io/shift-handover-intelligence/

---

**Good luck! 🚀**

If you need help, check the detailed `DEPLOYMENT_GUIDE.md` for more information.
