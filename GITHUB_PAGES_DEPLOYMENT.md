# 🚀 Frontend Deployment to GitHub Pages

## ✅ Prerequisites

Your backend is already live at:
```
https://shift-handover-intelligence-production.up.railway.app
```

## 📋 Step-by-Step Deployment Guide

### Step 1: Install Required Tools

```bash
# Install Angular CLI globally
npm install -g @angular/cli

# Or use npx (no global installation needed)
# npx will be used in the deployment script
```

### Step 2: Install Frontend Dependencies

```bash
cd /Users/shrinikatelu/shift-handover-project/frontend
npm install
```

### Step 3: Set Correct Base Href

The `package.json` already has the correct deployment script with base-href set:

```json
"deploy:gh-pages": "ng build --configuration production --base-href=/shift-handover-intelligence/ && ngh --dir=dist/frontend/browser --branch=gh-pages"
```

### Step 4: Run the Deployment Script

```bash
cd /Users/shrinikatelu/shift-handover-project

# Make the script executable
chmod +x deploy-frontend.sh

# Run the deployment
./deploy-frontend.sh
```

The script will:
1. ✅ Install dependencies
2. ✅ Build the production bundle with correct base-href
3. ✅ Deploy to gh-pages branch
4. ✅ Show you the live link

### Step 5: Verify GitHub Pages Settings

1. Go to: https://github.com/ShrinikaTelu/shift-handover-intelligence
2. Click **Settings** → **Pages**
3. Verify:
   - **Source**: Deploy from a branch
   - **Branch**: `gh-pages`
   - **Folder**: `/ (root)`
4. Click **Save**

### Step 6: Access Your Application

After deployment completes, your application will be live at:

```
https://ShrinikaTelu.github.io/shift-handover-intelligence/
```

## 🔗 Configuration Details

### Frontend URL
```
https://ShrinikaTelu.github.io/shift-handover-intelligence/
```

### Backend API URL
```
https://shift-handover-intelligence-production.up.railway.app
```

The frontend automatically uses the production backend URL when built with `--configuration production`.

## 📝 Environment Configuration

The frontend uses environment-based configuration:

**Development** (`environment.ts`):
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  healthUrl: 'http://localhost:8000/health'
};
```

**Production** (`environment.prod.ts`):
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://shift-handover-intelligence-production.up.railway.app/api',
  healthUrl: 'https://shift-handover-intelligence-production.up.railway.app/health'
};
```

## 🛠️ Manual Deployment (Alternative Method)

If you prefer to deploy manually without the script:

```bash
cd frontend

# Install dependencies
npm install

# Build with production configuration
npm run build:prod

# Deploy using angular-cli-ghpages
npx ngh --dir=dist/frontend/browser --branch=gh-pages --message="Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
```

## 🔄 Redeployment

To redeploy after making changes:

```bash
./deploy-frontend.sh
```

The script will rebuild and update the gh-pages branch automatically.

## ✅ Troubleshooting

### Issue: "dist/frontend/browser not found"
**Solution**: Make sure the build completed successfully and check the actual output directory name.

```bash
cd frontend
ls -la dist/
# Check the actual directory structure
```

### Issue: "GitHub Pages not showing latest changes"
**Solution**: GitHub Pages may take a few minutes to update. You can:
1. Hard refresh your browser (Cmd+Shift+R on Mac)
2. Clear browser cache
3. Wait 2-3 minutes for GitHub's CDN to update

### Issue: "API calls failing from production"
**Solution**: Verify the backend URL is correct and CORS is enabled in the backend:

```bash
# Test the backend
curl https://shift-handover-intelligence-production.up.railway.app/health
```

## 📊 Deployment Checklist

- [ ] Backend is live and running
- [ ] Backend returns health check response
- [ ] `environment.prod.ts` has correct backend URL
- [ ] `package.json` has correct base-href in deploy script
- [ ] Dependencies installed (`npm install`)
- [ ] Deployment script is executable (`chmod +x deploy-frontend.sh`)
- [ ] Ran deployment script (`./deploy-frontend.sh`)
- [ ] GitHub Pages settings configured to use gh-pages branch
- [ ] Application accessible at GitHub Pages URL

## 📞 Support

If you encounter issues:
1. Check the GitHub Pages settings in repository settings
2. Verify the gh-pages branch exists in your repository
3. Check browser console for CORS or API errors
4. Run `./deploy-frontend.sh` again with verbose output

---

**All set!** Your application is now deployed to GitHub Pages! 🎉
