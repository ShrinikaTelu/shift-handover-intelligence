# 🚀 Quick Start: Deploy to Railway in 5 Minutes

## Step 1: Sign Up on Railway
👉 Go to **https://railway.app** and sign up with GitHub

## Step 2: Create New Project
1. Click "Create New Project"
2. Select "Deploy from GitHub repo"
3. Search for `shift-handover-intelligence`
4. Click "Create" to auto-detect services

## Step 3: Configure Environment Variables

### For Backend Service
Click on the backend service and add these environment variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./handover.db
DEBUG=false
LOG_LEVEL=INFO
```

**⚠️ Important**: Replace `your_gemini_api_key_here` with your actual Gemini API key

### For Frontend Service
Click on the frontend service. No special variables needed - Railway detects Node.js automatically.

## Step 4: Wait for Deployment
Railway will automatically:
1. Detect your services (frontend and backend)
2. Build both applications
3. Deploy them

**Deployment time**: ~5-10 minutes

## Step 5: Get Your Live URLs

Once deployed, Railway will show you:
- **Frontend URL**: Click the "View" button on frontend service
- **Backend URL**: Click the "View" button on backend service

Example URLs:
```
Frontend: https://shift-handover-frontend-prod.railway.app
Backend:  https://shift-handover-backend-prod.railway.app
```

## Step 6: Update Frontend API Connection

After getting your backend URL:

1. Open `frontend/src/app/services/handover.service.ts`
2. Find this line:
   ```typescript
   private readonly API_URL = 'http://localhost:8000/api';
   ```
3. Replace it with your Railway backend URL:
   ```typescript
   private readonly API_URL = 'https://your-backend-url.railway.app/api';
   ```
4. Commit and push:
   ```bash
   git add .
   git commit -m "feat: update API URL for Railway deployment"
   git push origin main
   ```

## Step 7: Your App is Live! 🎉

Access your application at:
```
https://your-frontend-url.railway.app
```

Share this link just like your causalitycare project!

---

## Troubleshooting

### ❌ Frontend shows blank page
- Check browser console for errors (F12)
- Verify API URL is correct
- Check CORS settings

### ❌ API calls fail
- Go to Railway dashboard
- Click backend service
- Check logs for errors
- Verify environment variables are set

### ❌ Build failed
- Check build logs in Railway dashboard
- Ensure `package.json` and `requirements.txt` are correct
- Verify no syntax errors

---

## Additional Resources

📖 Full documentation: See `RAILWAY_DEPLOYMENT.md`
🔗 Railway docs: https://docs.railway.app
💬 Need help? Railway community: https://discord.gg/railway

---

## Next Deployment Steps (Optional)

- **Custom Domain**: Add your own domain (e.g., handover.yoursite.com)
- **Database**: Upgrade to PostgreSQL for production
- **Monitoring**: Set up alerts and logs
- **Auto-scaling**: Configure resource limits

