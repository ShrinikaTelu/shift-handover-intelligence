# 🚀 Shift Handover Intelligence - Deployment Guide

## ✅ Backend Status: LIVE ✅

Your backend is successfully deployed on Railway:
- **URL**: `https://shift-handover-intelligence-production.up.railway.app/`
- **API Status**: Working ✅
- **Health Check**: Available at `/health`

---

## 📱 Frontend Deployment to GitHub Pages

Your frontend will be deployed to: `https://ShrinikaTelu.github.io/shift-handover-intelligence/`

### Prerequisites

Make sure you have the following installed:
```bash
# Node.js and npm (should already have from development)
node --version    # Should be v25.2.1 or higher
npm --version     # Should be 10.x or higher

# Install Angular CLI globally (if not already installed)
npm install -g @angular/cli

# Install GitHub Pages deployment tool
npm install -g angular-cli-ghpages
```

### Quick Deployment Steps

**Step 1: Make the deployment script executable**
```bash
chmod +x deploy-frontend-gh-pages.sh
```

**Step 2: Run the deployment script**
```bash
./deploy-frontend-gh-pages.sh
```

**Step 3: Enter your backend URL when prompted**
```
Enter your Railway Backend URL (e.g., https://shift-handover-intelligence-production.up.railway.app): https://shift-handover-intelligence-production.up.railway.app
```

**Step 4: Wait for deployment to complete**
The script will:
- ✅ Update the API URL configuration
- ✅ Install dependencies
- ✅ Build the Angular project for production
- ✅ Deploy to GitHub Pages

**Step 5: Access your application**
- Frontend: `https://ShrinikaTelu.github.io/shift-handover-intelligence/`
- Backend API: `https://shift-handover-intelligence-production.up.railway.app/`
- API Documentation: `https://shift-handover-intelligence-production.up.railway.app/docs`

---

## 🔧 Manual Deployment (Alternative)

If you prefer to deploy manually instead of using the script:

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

### Step 2: Build for Production
```bash
npm run build:prod
```

### Step 3: Deploy to GitHub Pages
```bash
npm install -g angular-cli-ghpages
ngh --dir=dist/frontend/browser --branch=gh-pages
```

---

## ⚙️ Configuration Details

### Environment Variables

**Development** (`src/environments/environment.ts`):
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  healthUrl: 'http://localhost:8000/health'
};
```

**Production** (`src/environments/environment.prod.ts`):
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://shift-handover-intelligence-production.up.railway.app/api',
  healthUrl: 'https://shift-handover-intelligence-production.up.railway.app/health'
};
```

The build process automatically uses the correct environment based on the `--configuration production` flag.

---

## 🔐 CORS Configuration

Your backend is configured to accept requests from:
- Local development: `http://localhost:4200`
- Production: `https://ShrinikaTelu.github.io/`
- All origins (currently): `*`

For production, update the CORS settings in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ShrinikaTelu.github.io",  # Your GitHub Pages URL
        "https://shift-handover-intelligence-production.up.railway.app",  # Your API domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Build Information

When you run the build, you'll see:
```
Initial chunk files | Names         |  Raw size
main.js             | main          | 119.11 kB | 
polyfills.js        | polyfills     |  90.20 kB | 
styles.css          | styles        |   5.16 kB | 
                    | Initial total | 214.47 kB |
```

This is the production build size - it's optimized and minified.

---

## ⏱️ Deployment Timeline

1. **Script Execution**: ~2-3 minutes
   - Dependencies installation: ~1 minute
   - Build process: ~1 minute
   - GitHub Pages deployment: ~1 minute

2. **GitHub Pages Propagation**: ~1-2 minutes
   - Your site may not be immediately available
   - Check back after 2 minutes

3. **Total Time**: ~5 minutes from start to live

---

## ✨ Features Deployed

- ✅ Shift handover form with real-time generation
- ✅ PDF download capability
- ✅ Session history
- ✅ Gemini AI integration
- ✅ Database persistence
- ✅ Responsive Angular UI
- ✅ Security headers
- ✅ Gzip compression
- ✅ Static asset caching

---

## 🐛 Troubleshooting

### Build fails with permission error
```bash
chmod +x deploy-frontend-gh-pages.sh
```

### ngh command not found
```bash
npm install -g angular-cli-ghpages
```

### API returning 404 errors
- Check that the backend URL is correct
- Verify backend is running and accessible
- Check CORS settings in backend

### GitHub Pages showing old version
- Hard refresh browser: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
- Clear browser cache
- Check https://ShrinikaTelu.github.io/shift-handover-intelligence/

### Service showing "Unable to connect to API"
- Verify backend URL in environment files
- Check backend health: `https://shift-handover-intelligence-production.up.railway.app/health`
- Check browser console for CORS errors

---

## 📝 Next Steps

1. ✅ Run the deployment script
2. ✅ Test the frontend at the GitHub Pages URL
3. ✅ Generate a test handover
4. ✅ Download PDF to verify functionality
5. ✅ Share your live application!

---

## 🎉 Success Checklist

- [ ] Backend is live on Railway
- [ ] Frontend deployment script runs successfully
- [ ] GitHub Pages site is accessible
- [ ] API calls work from frontend
- [ ] PDF generation works
- [ ] No console errors
- [ ] All features functioning

---

**Questions or issues?** Check the build logs for detailed error messages!
