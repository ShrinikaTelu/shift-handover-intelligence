# Shift Handover Intelligence - Deployment Guide

## 🎯 Overview

This guide explains how to deploy the **Shift Handover Intelligence** application with:
- **Frontend**: Deployed on **GitHub Pages** (like CausalityCare)
- **Backend**: Deployed on **Railway.app**
- **Live URL**: `https://ShrinikaTelu.github.io/shift-handover-intelligence/`

---

## 📋 Prerequisites

### Required Tools & Accounts

1. **GitHub Account** - Already have this ✓
2. **Railway Account** - Create at [railway.app](https://railway.app)
3. **Local Tools**:
   - Node.js 18+ (for Angular build)
   - Python 3.9+ (for backend)
   - Git
   - Angular CLI: `npm install -g @angular/cli`
   - GitHub Pages CLI: Already handled by `angular-cli-ghpages`

### API Keys

- **Gemini API Key** - Get from [ai.google.dev](https://ai.google.dev)

---

## 🚀 Deployment Steps

### Step 1: Setup GitHub Pages Repository Settings

1. Go to GitHub: https://github.com/ShrinikaTelu/shift-handover-intelligence
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under "Build and deployment":
   - Source: Select **Deploy from a branch**
   - Branch: **gh-pages** (this will be created automatically)
5. Save the settings

### Step 2: Prepare for Deployment

Make sure you're on the `feature/shift-handover-intelligence` branch:

```bash
cd /Users/shrinikatelu/shift-handover-project

# Switch to feature branch
git checkout feature/shift-handover-intelligence

# Pull latest changes
git pull origin feature/shift-handover-intelligence
```

### Step 3: Setup Railway for Backend

#### 3.1 Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "GitHub Repo" and authenticate
4. Choose repository: `shift-handover-intelligence`
5. Click "Deploy"

#### 3.2 Configure Backend Service

Railway will automatically detect the `Dockerfile` in the root directory.

1. In Railway dashboard, click on the `shift-handover-intelligence` service
2. Go to **Settings**
3. Set **Dockerfile**: `./Dockerfile` (should auto-detect)
4. Set **Build context**: `.` (root directory)
5. Set **Port**: `8000`

#### 3.3 Add Environment Variables

In Railway dashboard, go to **Variables**:

```
GEMINI_API_KEY=your_gemini_api_key_here
DEBUG=false
ALLOWED_ORIGINS=*
DATABASE_URL=sqlite+aiosqlite:///./handover.db
```

#### 3.4 Deploy

Click **Deploy** button. Railway will:
- Build the Docker image
- Deploy the backend
- Provide you with a URL like: `https://shift-handover-backend-xxx.up.railway.app`

⚠️ **Save this URL** - you'll need it for the frontend!

---

### Step 4: Deploy Frontend to GitHub Pages

#### 4.1 Quick Deployment Script

Use the provided `deploy.sh` script:

```bash
cd /Users/shrinikatelu/shift-handover-project

# Make script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

The script will:
1. Ask for your Railway backend URL
2. Update the frontend API endpoint
3. Build the Angular app for production
4. Deploy to GitHub Pages
5. Give you the final URLs

#### 4.2 Manual Deployment (Alternative)

If the script doesn't work, do it manually:

```bash
# Step 1: Update API endpoint in frontend
# Edit: frontend/src/app/services/handover.service.ts
# Replace: private apiUrl = 'http://localhost:8000';
# With: private apiUrl = 'https://shift-handover-backend-xxx.up.railway.app';

# Step 2: Install dependencies
cd frontend
npm install

# Step 3: Build for production
ng build --configuration production --base-href "/shift-handover-intelligence/"

# Step 4: Deploy to GitHub Pages
npx angular-cli-ghpages --dir=dist/shift-handover-intelligence --repo=https://github.com/ShrinikaTelu/shift-handover-intelligence.git
```

---

## ✅ Verification

After deployment, verify everything works:

### 1. Frontend
Visit: `https://ShrinikaTelu.github.io/shift-handover-intelligence/`

You should see the Shift Handover Intelligence application.

### 2. Backend API
- API Docs: `https://shift-handover-backend-xxx.up.railway.app/docs`
- Health Check: `https://shift-handover-backend-xxx.up.railway.app/health`

### 3. Test Connection
From the frontend, try to create a handover and verify:
- The form submits
- The backend processes the request
- PDF is generated
- Response displays in the application

---

## 🐳 Docker Information

The deployment uses Docker with:

**File**: `Dockerfile` (at root level)

**Key Points**:
- Base image: `python:3.9-slim`
- Copies backend code from `./backend/`
- Installs dependencies from `backend/requirements.txt`
- Exposes port `8000`
- Includes health check
- Railway automatically handles:
  - Building the image
  - Running the container
  - Scaling & port mapping
  - SSL certificates

**.dockerignore** File:
- Excludes `node_modules`, `.git`, venv, etc.
- Reduces image size
- Faster deployments

---

## 📚 Project Structure for Deployment

```
shift-handover-project/
├── Dockerfile                 # Backend containerization
├── .dockerignore             # Docker build optimization
├── deploy.sh                 # Deployment automation script
│
├── backend/                  # FastAPI backend
│   ├── main.py
│   ├── requirements.txt      # Python dependencies
│   └── ...
│
├── frontend/                 # Angular frontend
│   ├── src/
│   │   └── app/
│   │       └── services/
│   │           └── handover.service.ts  # API configuration
│   ├── angular.json
│   ├── package.json
│   └── ...
│
├── sample-data/              # Test data
└── README.md                 # Documentation
```

---

## 🔧 Environment Variables Reference

### Backend (Railway)
| Variable | Value | Required |
|----------|-------|----------|
| `GEMINI_API_KEY` | Your API key | ✓ Yes |
| `DEBUG` | `false` (production) | Optional |
| `DATABASE_URL` | `sqlite+aiosqlite:///./handover.db` | Optional |
| `ALLOWED_ORIGINS` | `*` or specific domain | Optional |

### Frontend (Build-time only)
No environment variables needed - the Railway API URL is hardcoded after build.

---

## 🚨 Troubleshooting

### Issue: Frontend shows 404 errors

**Solution**: 
- Check base-href in build command: `--base-href "/shift-handover-intelligence/"`
- Verify GitHub Pages is enabled in repository settings
- Wait 2-3 minutes for GitHub Pages to redeploy

### Issue: API calls fail with CORS errors

**Solution**:
- In Railway, ensure `ALLOWED_ORIGINS=*` is set
- Check backend is running: `https://shift-handover-backend-xxx.up.railway.app/health`
- Verify frontend has correct API URL

### Issue: Backend won't start on Railway

**Solution**:
- Check logs in Railway dashboard
- Verify `Dockerfile` path is correct
- Ensure `GEMINI_API_KEY` environment variable is set
- Check `requirements.txt` has all dependencies

### Issue: PDF generation fails

**Solution**:
- Ensure `reportlab` is installed in backend
- Check logs for error messages
- Verify backend has enough memory (Railway default should be OK)

---

## 📈 Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Deploy frontend to GitHub Pages
3. ✅ Test the complete flow
4. 📤 Share the live link: `https://ShrinikaTelu.github.io/shift-handover-intelligence/`
5. 🔄 Push code changes to `feature/shift-handover-intelligence` branch
6. 📝 Create Pull Request to `main` when ready

---

## 🔗 Useful Links

- **Railway Dashboard**: https://railway.app
- **GitHub Pages Settings**: https://github.com/ShrinikaTelu/shift-handover-intelligence/settings/pages
- **Live Application**: https://ShrinikaTelu.github.io/shift-handover-intelligence/
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Angular Deployment**: https://angular.io/guide/deployment

---

## 📞 Support

If you encounter issues:

1. Check Railway logs: Dashboard → Service → Logs
2. Check GitHub Pages deployment: Repo → Settings → Pages → Deployments
3. Test API directly: Use Swagger UI at backend URL `/docs`
4. Review this guide and check troubleshooting section

---

**Last Updated**: January 12, 2026  
**Version**: 1.0.0  
**Status**: Ready for Deployment
