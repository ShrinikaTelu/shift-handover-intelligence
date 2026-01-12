# 🎯 Shift Handover Intelligence - Deployment Instructions

## Summary of What's Been Setup

I've analyzed your **causalitycare** deployment approach and configured the same for your **shift-handover-intelligence** project. Here's what's been done:

---

## ✅ What's Been Prepared

### 1. **Docker Configuration** ✓
- **File**: `Dockerfile` (at root level)
- **Base**: Python 3.9-slim
- **Features**:
  - Copies backend code
  - Installs Python dependencies
  - Exposes port 8000
  - Includes health checks
  - Railway will auto-detect and deploy

### 2. **Docker Ignore** ✓
- **File**: `.dockerignore`
- **Purpose**: Reduces image size, speeds up deployment

### 3. **Deployment Scripts** ✓
- **File**: `deploy.sh`
- **What it does**:
  - Updates frontend API endpoint to your Railway URL
  - Builds Angular for production
  - Deploys to GitHub Pages
  - Provides final live links

### 4. **Comprehensive Guides** ✓
- **DEPLOYMENT_GUIDE.md**: Detailed step-by-step guide
- **RAILWAY_SETUP.md**: Quick 5-minute Railway setup

---

## 🚀 Your Deployment Architecture (Same as CausalityCare)

```
┌──────────────────────────────────┐
│    GitHub Pages (Frontend)       │
│   https://ShrinikaTelu.         │
│   github.io/shift-handover-     │
│   intelligence/                  │
│                                  │
│  • Angular App                   │
│  • Static Files                  │
│  • Fast CDN Delivery             │
└────────────┬─────────────────────┘
             │
             │ (API Calls)
             │
┌────────────▼─────────────────────┐
│     Railway.app (Backend)        │
│  https://shift-handover-         │
│  backend-xyz.up.railway.app      │
│                                  │
│  • FastAPI Server                │
│  • Python 3.9                    │
│  • SQLite Database               │
│  • Gemini AI Integration         │
│  • PDF Generation                │
└──────────────────────────────────┘
```

---

## 📋 Step-by-Step Deployment Instructions

### Step 1️⃣: Enable GitHub Pages

1. Go to: https://github.com/ShrinikaTelu/shift-handover-intelligence
2. Click **Settings** → **Pages** (left sidebar)
3. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **gh-pages** (will be created automatically)
4. Click **Save**

✅ **GitHub Pages is now ready to receive deployments**

---

### Step 2️⃣: Setup Railway Backend (5 minutes)

#### 2a. Create Railway Project
1. Go to https://railway.app
2. Sign up with GitHub
3. Click **New Project** → **GitHub Repo**
4. Select: `shift-handover-intelligence`
5. Railway will auto-detect the Dockerfile and start deployment

#### 2b. Add Environment Variables
In Railway Dashboard:
1. Find your service (named after the Dockerfile)
2. Go to **Variables** tab
3. Add these:

```
GEMINI_API_KEY=your_api_key_from_ai.google.dev
DEBUG=false
DATABASE_URL=sqlite+aiosqlite:///./handover.db
ALLOWED_ORIGINS=*
```

#### 2c. Get Your Backend URL
1. Wait for deployment (2-3 minutes)
2. Copy the provided URL (looks like):
   ```
   https://shift-handover-backend-xxx.up.railway.app
   ```
3. **Save this URL** - you'll need it next!

✅ **Backend is now LIVE!**

---

### Step 3️⃣: Deploy Frontend to GitHub Pages (2 minutes)

#### Option A: Using the Script (Easiest)

```bash
cd /Users/shrinikatelu/shift-handover-project

chmod +x deploy.sh
./deploy.sh
```

When prompted, paste your Railway backend URL from Step 2.

The script will:
- Update frontend API endpoint
- Build Angular for production
- Deploy to GitHub Pages
- Print your live URL

#### Option B: Manual Deployment

```bash
cd /Users/shrinikatelu/shift-handover-project

# Step 1: Update the API URL in frontend code
# File: frontend/src/app/services/handover.service.ts
# Find: private apiUrl = 'http://localhost:8000';
# Replace with: private apiUrl = 'https://shift-handover-backend-xxx.up.railway.app';

# Step 2: Build
cd frontend
npm install
ng build --configuration production --base-href "/shift-handover-intelligence/"

# Step 3: Deploy
npx angular-cli-ghpages --dir=dist/shift-handover-intelligence --repo=https://github.com/ShrinikaTelu/shift-handover-intelligence.git
```

✅ **Frontend is now LIVE on GitHub Pages!**

---

## 🎉 Your Final Live URLs

After deployment, you'll have:

**Frontend (GitHub Pages):**
```
https://ShrinikaTelu.github.io/shift-handover-intelligence/
```

**Backend API (Railway):**
```
https://shift-handover-backend-xxx.up.railway.app
```

**API Documentation (Swagger):**
```
https://shift-handover-backend-xxx.up.railway.app/docs
```

This matches what you wanted - a live link like your CausalityCare! 🎊

---

## 🔄 How Auto-Updates Work

**Once deployed:**

1. You push code to `feature/shift-handover-intelligence`
2. Railway automatically pulls changes → rebuilds → redeploys backend
3. When you run `deploy.sh`, GitHub Pages gets updated frontend

**No manual deployment needed after initial setup!**

---

## 📚 File Reference

| File | Purpose | Status |
|------|---------|--------|
| `Dockerfile` | Backend containerization | ✅ Created |
| `.dockerignore` | Optimize Docker build | ✅ Created |
| `deploy.sh` | Frontend deployment automation | ✅ Updated |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment guide | ✅ Created |
| `RAILWAY_SETUP.md` | Quick Railway setup (5 min) | ✅ Created |

---

## 🔐 Environment Variables

### Backend (Set in Railway Dashboard)

```env
# Required
GEMINI_API_KEY=your_key_from_ai.google.dev

# Optional (but recommended)
DEBUG=false
DATABASE_URL=sqlite+aiosqlite:///./handover.db
ALLOWED_ORIGINS=*
```

### Frontend
No environment variables - API URL is hardcoded during build.

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] GitHub Pages is enabled in repository settings
- [ ] Railway backend is running (check dashboard)
- [ ] Frontend loads at GitHub Pages URL
- [ ] Backend API is accessible at Railway URL
- [ ] Swagger UI works: `backend-url/docs`
- [ ] Frontend can call backend API (test from the app)
- [ ] PDF generation works in the application

---

## 🐛 Common Issues & Solutions

### Issue: Frontend shows "Cannot GET /"
**Solution**: GitHub Pages caching. Wait 2-3 minutes or hard refresh (Cmd+Shift+R)

### Issue: API calls fail with CORS error
**Solution**: 
- Check `ALLOWED_ORIGINS=*` is set in Railway
- Verify backend URL in `handover.service.ts`

### Issue: Backend won't deploy on Railway
**Solution**:
- Check Railway logs for errors
- Ensure `GEMINI_API_KEY` is set
- Verify `Dockerfile` exists at root

### Issue: PDF generation fails
**Solution**:
- Check backend logs in Railway
- Ensure all Python dependencies installed
- Try creating handover with simple text first

---

## 📖 Additional Resources

- **Railway Setup**: `RAILWAY_SETUP.md` (this directory)
- **Detailed Guide**: `DEPLOYMENT_GUIDE.md` (this directory)
- **Railway Docs**: https://docs.railway.app/
- **Angular Deployment**: https://angular.io/guide/deployment
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **GitHub Pages**: https://pages.github.com/

---

## 🎯 Next Steps

1. **Read** `RAILWAY_SETUP.md` for the quick 5-minute setup
2. **Follow** the step-by-step instructions above
3. **Deploy** backend on Railway
4. **Deploy** frontend using `deploy.sh`
5. **Test** your live application
6. **Share** the GitHub Pages URL!

---

## 💡 Tips

- **Keep your API key secure** - Use Railway's secrets feature
- **Monitor deployments** - Check Railway dashboard regularly
- **Test locally first** - Run locally with `npm start` + backend
- **Update frontend URL** - Each time you redeploy backend to different Railway instance
- **Version control** - Commit all changes to feature branch

---

**You're all set! Your application deployment is now as professional as CausalityCare. 🚀**

*Last updated: January 12, 2026*
