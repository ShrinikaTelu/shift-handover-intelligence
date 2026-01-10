# 🚀 Railway.app Deployment Guide - Complete Setup

> Deploy Shift Handover Intelligence to production in 10 minutes using Railway.app

---

## Why Railway.app?

✅ **Best for this project** because:
- Free tier (up to 5GB/month)
- GitHub integration (auto-deploy)
- Built-in database support (PostgreSQL, MySQL, SQLite)
- Easy environment variable management
- Docker support
- Global CDN
- 99.9% uptime SLA

---

## Step-by-Step Deployment

### 1. Prepare Your Code

#### 1.1 Create GitHub Repository
```bash
cd /Users/shrinikatelu/shift-handover-project

# Initialize git if not already done
git init

# Add all files
git add .

# Create .gitignore (if not exists)
cat > .gitignore << 'EOF'
# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node/Frontend
node_modules/
npm-debug.log
yarn-error.log
dist/
.angular/
*.swp

# IDE
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/
EOF

# Commit
git commit -m "Initial commit: Shift Handover Intelligence"

# Add to GitHub
# Go to https://github.com/new and create repository
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/shift-handover-intelligence.git
git branch -M main
git push -u origin main
```

#### 1.2 Verify .env.example exists
```bash
cat .env.example
# Should show template with GOOGLE_API_KEY, etc.
```

---

### 2. Create Railway Project

#### 2.1 Sign Up
1. Go to [railway.app](https://railway.app)
2. Click "Start Now"
3. Sign in with GitHub
4. Authorize Railway

#### 2.2 Create New Project
```
Dashboard → New Project → GitHub Repo
```

#### 2.3 Select Repository
1. Search for `shift-handover-intelligence`
2. Click to select
3. Authorize Railway to access repo

---

### 3. Configure Services

#### 3.1 Backend Service (FastAPI)

**Create service:**
```
Project → New → GitHub Repo
→ Select: backend folder
```

**Configure:**
```
Service Name: shift-handover-backend
Root Directory: ./backend
Runtime: Python 3.9
```

**Build & Start Commands:**
```
Build: pip install -r requirements.txt
Start: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
```
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
DATABASE_URL=sqlite+aiosqlite:///./handovers.db
ENVIRONMENT=production
```

#### 3.2 Frontend Service (Angular)

**Option A: Using Vercel (Recommended)**
```
Skip Railway for frontend
Deploy to Vercel instead (see below)
```

**Option B: Using Railway**
```
Service Name: shift-handover-frontend
Root Directory: ./frontend
Runtime: Node.js
```

**Build & Start Commands:**
```
Build: npm install && npm run build
Start: npx http-server dist/browser -p $PORT
```

**Environment Variables:**
```
API_URL=https://your-backend-url.railway.app
```

---

### 4. Deploy via Railway CLI (Alternative)

#### 4.1 Install Railway CLI
```bash
npm i -g @railway/cli
# or
brew install railway
```

#### 4.2 Login
```bash
railway login
```

#### 4.3 Deploy
```bash
cd /Users/shrinikatelu/shift-handover-project

# Link to project
railway link

# Deploy
railway up

# View logs
railway logs
```

---

### 5. Deploy Frontend to Vercel (Recommended)

#### 5.1 Sign Up
```
Go to vercel.com
Sign in with GitHub
```

#### 5.2 Import Project
```
Dashboard → Add New → Project
→ Import Git Repository
→ Select shift-handover-intelligence
```

#### 5.3 Configure
```
Framework: Angular
Root Directory: ./frontend
Build Command: npm run build
Output Directory: dist/browser
```

#### 5.4 Environment Variables
```
ANGULAR_APP_API_URL=https://your-backend-url.railway.app
```

#### 5.5 Deploy
```
Click "Deploy"
Wait 2-3 minutes
```

---

## 🔐 Set Environment Variables

### Backend (Railway Dashboard)

```
Project → shift-handover-backend → Settings → Variables
```

Add these variables:

| Key | Value | Description |
|-----|-------|-------------|
| `GOOGLE_API_KEY` | `AIzaSy...` | Your Gemini API key |
| `GEMINI_MODEL` | `gemini-3-flash-preview` | Model version |
| `DATABASE_URL` | `sqlite+aiosqlite:///./handovers.db` | Database |
| `ENVIRONMENT` | `production` | Environment type |
| `LOG_LEVEL` | `INFO` | Logging level |

⚠️ **IMPORTANT**: Never commit these values to GitHub!

### Frontend (Vercel Dashboard)

```
Project → Settings → Environment Variables
```

Add:

| Key | Value |
|-----|-------|
| `ANGULAR_APP_API_URL` | `https://backend-url.railway.app` |

Update `frontend/src/app/services/handover.service.ts`:
```typescript
// Add to environment.ts and environment.prod.ts
export const environment = {
  production: true,
  apiUrl: process.env['ANGULAR_APP_API_URL'] || 'http://localhost:8000'
};

// In handover.service.ts
private readonly API_URL = environment.apiUrl + '/api';
```

---

## 📊 Monitor Deployment

### Railway Dashboard

```
Project → Services → shift-handover-backend
```

Check:
- ✅ Deployment Status
- ✅ Memory Usage
- ✅ CPU Usage
- ✅ Network
- ✅ Recent Logs

### Useful Commands

```bash
# View live logs
railway logs --follow

# View service status
railway status

# Check environment
railway env

# Open dashboard
railway open
```

---

## 🧪 Test Deployed Application

### Test Backend

```bash
# Health check
curl https://YOUR_BACKEND_URL.railway.app/health

# Generate handover
curl -X POST https://YOUR_BACKEND_URL.railway.app/api/handover/generate \
  -H "Content-Type: application/json" \
  -d '{
    "shift_notes": "Test shift notes",
    "alarms_json": null,
    "trends_csv": null
  }'
```

### Test Frontend

```
Open: https://shift-handover.vercel.app

1. Enter shift notes
2. Click "Generate"
3. Check if report appears
```

### Verify Integration

```
Frontend should connect to Backend
Check browser console for any errors
```

---

## 🔧 Troubleshooting

### Backend won't deploy

**Error**: `ModuleNotFoundError: No module named 'main'`

**Solution**:
```
1. Check requirements.txt is in backend folder
2. Verify build command: pip install -r requirements.txt
3. Verify start command includes full path if needed
```

### Frontend can't reach backend

**Error**: `CORS error` or `Connection refused`

**Solution**:
```
1. Update API_URL in service to deployed backend URL
2. Ensure backend is public (not private network)
3. Check CORS is enabled in backend
4. Verify firewall allows HTTPS
```

### Database errors

**Error**: `sqlite3.OperationalError: database is locked`

**Solution**:
```
1. Use PostgreSQL instead:
   DATABASE_URL=postgresql://user:pass@db.railway.app/dbname

2. Or configure SQLite with WAL mode:
   DATABASE_URL=sqlite+aiosqlite:///./handovers.db?journal_mode=WAL
```

### API key not working

**Error**: `Invalid API key`

**Solution**:
```
1. Get new key from ai.google.dev
2. Verify key is correct (no extra spaces)
3. Ensure GOOGLE_API_KEY variable is set
4. Restart service after changing variable
```

---

## 📈 Scaling Considerations

### When to upgrade from free tier:

| Metric | Free Limit | Action |
|--------|-----------|--------|
| Storage | 5GB | Upgrade to Pro ($5/month) |
| Memory | 0.5GB RAM | Upgrade to Pro |
| CPU | Shared | Upgrade to Pro |
| Bandwidth | 100GB/month | Upgrade or optimize |

### Optimization tips:

1. **Use PostgreSQL instead of SQLite** (scales better)
2. **Enable database caching** (reduce API calls)
3. **Implement rate limiting** (prevent abuse)
4. **Use CDN for frontend** (Vercel does this)
5. **Compress API responses** (gzip)

---

## 🔄 Continuous Deployment

### Auto-deploy from GitHub

Railway automatically redeploys when you push to main:

```bash
# Make changes
git add .
git commit -m "Fix: improve performance"
git push origin main

# Railway will automatically:
# 1. Detect changes
# 2. Build new images
# 3. Deploy to production
# 4. Zero downtime deployment
```

### Manual redeploy if needed

```
Railway Dashboard → Service → Redeploy
```

---

## 📝 Production Checklist

Before going live:

- [ ] Environment variables set correctly
- [ ] API key has necessary permissions
- [ ] Database initialized
- [ ] CORS configured properly
- [ ] Error handling working
- [ ] Logging enabled
- [ ] Backups configured
- [ ] Monitoring alerts set up
- [ ] Custom domain configured (optional)
- [ ] SSL/HTTPS enabled (automatic)

---

## 🎉 Success!

Your application is now live:

**Backend**: `https://shift-handover-backend-prod.railway.app`
**Frontend**: `https://shift-handover.vercel.app`

Share these URLs for the hackathon submission! 🏆

---

## 📞 Railway Support

- **Docs**: https://docs.railway.app
- **Discord**: https://railway.app/discord
- **Status**: https://status.railway.app
- **Pricing**: https://railway.app/pricing

---

## 💡 Pro Tips

1. **Use Railway CLI for faster iterations**
   ```bash
   railway up  # Deploy immediately
   ```

2. **Monitor logs in real-time**
   ```bash
   railway logs -f  # Follow mode
   ```

3. **Pull production environment locally**
   ```bash
   railway env | cat > .env.production
   ```

4. **Roll back to previous deployment**
   ```
   Dashboard → Service → Deployments → Select older → Redeploy
   ```

5. **Set up alerts for errors**
   ```
   Project → Alerts → Add notification webhook
   ```

---

<div align="center">

**🚀 Deployment Complete!**

Your Shift Handover Intelligence app is now live and ready for the Gemini 3 Hackathon

</div>
