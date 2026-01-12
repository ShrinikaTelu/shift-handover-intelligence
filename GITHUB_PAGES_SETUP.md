# GitHub Pages Deployment Guide

This project is configured to automatically deploy to GitHub Pages.

## Current Setup

Your project will be deployed to:
```
https://ShrinikaTelu.github.io/shift-handover-intelligence/
```

## How It Works

1. **Automatic Deployment**: Every time you push to the `main` branch, GitHub Actions automatically:
   - Builds your Angular frontend
   - Deploys it to GitHub Pages

2. **GitHub Actions Workflow**: The `.github/workflows/deploy-github-pages.yml` file handles:
   - Checking out your code
   - Installing Node.js dependencies
   - Building the Angular app with the correct base href
   - Uploading the build artifacts
   - Deploying to GitHub Pages

## Configuration Changes Made

### 1. Angular Configuration (`frontend/angular.json`)
- Added `"baseHref": "/shift-handover-intelligence/"` to the build options
- This ensures all routes work correctly on GitHub Pages

### 2. GitHub Actions Workflow (`.github/workflows/deploy-github-pages.yml`)
- Triggered on push to `main` branch
- Builds production-ready Angular bundle
- Automatically deploys to GitHub Pages

## Enable GitHub Pages

1. Go to your repository settings: https://github.com/ShrinikaTelu/shift-handover-intelligence/settings/pages
2. Under "Build and deployment":
   - Source: Select "GitHub Actions"
3. Save

## Deployment Status

After pushing these changes:
1. Go to your repository's "Actions" tab
2. Look for the "Deploy to GitHub Pages" workflow
3. Once it completes successfully, your app will be live at:
   ```
   https://ShrinikaTelu.github.io/shift-handover-intelligence/
   ```

## Local Testing

To test the build locally:
```bash
cd frontend
npm run build -- --configuration production
```

Then view the built files in `frontend/dist/frontend/`

## Notes

- The frontend build is deployed to GitHub Pages
- The backend API is separate and should be hosted elsewhere (Docker, Heroku, etc.)
- Update the API endpoint in your service files if using a different backend URL in production
