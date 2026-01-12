# 🚀 Quick Deployment Commands

## Your Live Application Links

### ✅ Backend (Already Deployed on Railway)
- **URL**: https://shift-handover-intelligence-production.up.railway.app/
- **API Base**: https://shift-handover-intelligence-production.up.railway.app/api
- **API Docs**: https://shift-handover-intelligence-production.up.railway.app/docs

### 📱 Frontend (Deploy to GitHub Pages)
- **Target URL**: https://shrinikatelu.github.io/shift-handover-intelligence/

---

## 📋 Prerequisites

```bash
# Install global tools
npm install -g @angular/cli
npm install -g angular-cli-ghpages
```

---

## 🚀 Deploy Frontend (One Command)

```bash
# Navigate to project root
cd /Users/shrinikatelu/shift-handover-project

# Make the script executable
chmod +x deploy-github-pages.sh

# Run deployment
./deploy-github-pages.sh
```

That's it! The script will:
1. Install dependencies
2. Build the production-ready Angular app
3. Deploy to GitHub Pages
4. Display your live URLs

---

## 📊 What Gets Deployed

### Frontend (GitHub Pages)
- Built Angular application
- Configured to use Railway backend
- Served from: `https://shrinikatelu.github.io/shift-handover-intelligence/`

### Backend (Railway)
- FastAPI server with Gemini integration
- SQLite database
- Already running on: `https://shift-handover-intelligence-production.up.railway.app/`

---

## 🔗 API Endpoints

All available at: `https://shift-handover-intelligence-production.up.railway.app/`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Check backend health |
| `/api/handover/generate` | POST | Generate handover with AI |
| `/api/handover/{session_id}` | GET | Get handover by session ID |
| `/api/handover/{session_id}/download-pdf` | GET | Download handover as PDF |
| `/docs` | GET | Swagger UI documentation |

---

## ✨ Features

- ✅ AI-powered shift handover generation (Gemini)
- ✅ PDF export functionality
- ✅ Session management
- ✅ Angular frontend with responsive UI
- ✅ FastAPI backend with async support
- ✅ SQLite database for persistence
- ✅ CORS enabled for frontend integration

---

## 🛠️ Git Workflow

Current Branch: `feature/shift-handover-intelligence`

```bash
# View current branch
git branch

# See deployment history
git log --oneline -10
```

---

## 📝 Next Steps After Deployment

1. Visit: https://shrinikatelu.github.io/shift-handover-intelligence/
2. Test the handover form
3. Generate a sample handover
4. Download as PDF
5. Share the live link!

---

## 🆘 Troubleshooting

### Issue: 404 Not Found
- **Cause**: GitHub Pages still building
- **Solution**: Wait 1-2 minutes and refresh

### Issue: API Connection Failed
- **Cause**: Backend down or CORS issue
- **Solution**: Check https://shift-handover-intelligence-production.up.railway.app/health

### Issue: Blank Page
- **Cause**: Browser cache
- **Solution**: Hard refresh (Cmd+Shift+R on Mac)

### Issue: Build Fails
- **Cause**: Missing dependencies
- **Solution**: Run `npm install` in frontend folder first

---

## 📞 Support

- **Frontend Repository**: https://github.com/ShrinikaTelu/shift-handover-intelligence
- **GitHub Pages Settings**: https://github.com/ShrinikaTelu/shift-handover-intelligence/settings/pages
- **Railway Dashboard**: https://railway.app/dashboard

---

**Last Updated**: January 12, 2026
**Version**: 1.0.0
