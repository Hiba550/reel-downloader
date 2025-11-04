# 🚀 Azure Deployment Guide - Reel Downloader

## 📋 Prerequisites

- **Azure Account** (free tier works fine)
- **Azure CLI** installed (or use Azure Portal)
- **Git** installed on your computer

---

## 🎯 Method 1: Deploy via Azure Portal (Easiest)

### Step 1: Create Azure App Service

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **"Create a resource"**
3. Search for **"Web App"** and click **Create**

### Step 2: Configure Web App

Fill in the following details:

| Setting | Value |
|---------|-------|
| **Subscription** | Your Azure subscription |
| **Resource Group** | Create new: `reel-downloader-rg` |
| **Name** | `reel-downloader-app` (must be unique) |
| **Publish** | Code |
| **Runtime stack** | Python 3.11 |
| **Operating System** | Linux |
| **Region** | Choose nearest to you |
| **Pricing Plan** | B1 Basic ($13/month) or F1 Free |

4. Click **"Review + Create"** → **"Create"**
5. Wait 2-3 minutes for deployment

### Step 3: Configure Deployment

1. Go to your Web App resource
2. In left menu, click **"Deployment Center"**
3. Choose deployment source:

#### Option A: GitHub (Recommended)
- Select **GitHub**
- Authorize Azure to access your GitHub
- Select your repository
- Select branch (usually `main` or `master`)
- Click **Save**

#### Option B: Local Git
- Select **Local Git**
- Click **Save**
- Copy the Git URL shown

### Step 4: Configure Application Settings

1. In left menu, click **"Configuration"**
2. Click **"General settings"** tab
3. Set **Startup Command**: `gunicorn --bind=0.0.0.0 --timeout 600 --workers=2 app:app`
4. Click **Save**

### Step 5: Deploy Your Code

#### If using GitHub:
- Push your code to GitHub
- Azure will auto-deploy on every push

#### If using Local Git:
```powershell
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit"

# Add Azure remote
git remote add azure <YOUR_AZURE_GIT_URL>

# Deploy
git push azure main
```

### Step 6: Verify Deployment

1. Go to **"Overview"** in your Web App
2. Click the **URL** (e.g., `https://reel-downloader-app.azurewebsites.net`)
3. Your app should be live! 🎉

---

## 🎯 Method 2: Deploy via Azure CLI (Advanced)

### Step 1: Install Azure CLI

```powershell
# If not installed, download from:
# https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows
```

### Step 2: Login to Azure

```powershell
az login
```

### Step 3: Create Resource Group

```powershell
az group create --name reel-downloader-rg --location eastus
```

### Step 4: Create App Service Plan

```powershell
# Free tier
az appservice plan create --name reel-downloader-plan --resource-group reel-downloader-rg --sku F1 --is-linux

# OR Basic tier (better performance)
az appservice plan create --name reel-downloader-plan --resource-group reel-downloader-rg --sku B1 --is-linux
```

### Step 5: Create Web App

```powershell
az webapp create --resource-group reel-downloader-rg --plan reel-downloader-plan --name reel-downloader-app --runtime "PYTHON:3.11"
```

### Step 6: Configure Startup Command

```powershell
az webapp config set --resource-group reel-downloader-rg --name reel-downloader-app --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 --workers=2 app:app"
```

### Step 7: Deploy from Local Git

```powershell
# Configure deployment user (first time only)
az webapp deployment user set --user-name <username> --password <password>

# Get Git deployment URL
az webapp deployment source config-local-git --name reel-downloader-app --resource-group reel-downloader-rg

# Deploy
git remote add azure <output_url_from_above>
git push azure main
```

---

## 🎯 Method 3: Deploy via VS Code (Quickest)

### Step 1: Install Azure Extension

1. Open VS Code
2. Install **"Azure App Service"** extension
3. Sign in to Azure

### Step 2: Deploy

1. Right-click on your project folder
2. Select **"Deploy to Web App..."**
3. Follow the prompts:
   - Create new Web App
   - Enter unique name
   - Select Python 3.11
   - Select pricing tier
4. VS Code deploys automatically! 🚀

---

## ⚙️ Important Configuration

### Enable HTTPS (Required for PWA)

1. In Azure Portal → Your Web App
2. Go to **"TLS/SSL settings"**
3. **HTTPS Only**: Set to **ON**
4. Your app is now: `https://your-app.azurewebsites.net`

### Configure Session Secret (Security)

1. Go to **"Configuration"** → **"Application settings"**
2. Click **"+ New application setting"**
3. Add:
   - **Name**: `SECRET_KEY`
   - **Value**: (generate a random string)
4. Update `app.py`:

```python
import os
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))
```

### Set Download Retention

1. In **"Configuration"** → **"Application settings"**
2. Add:
   - **Name**: `DOWNLOAD_RETENTION_HOURS`
   - **Value**: `6` (or any number)

---

## 📱 Update PWA for Azure URL

After deployment, update these files with your Azure URL:

### `static/manifest.json`

```json
{
  "name": "Reel Downloader",
  "short_name": "Reel DL",
  "start_url": "https://your-app.azurewebsites.net/",
  "scope": "https://your-app.azurewebsites.net/",
  "share_target": {
    "action": "https://your-app.azurewebsites.net/share-target",
    ...
  }
}
```

### Redeploy after changes:
```powershell
git add .
git commit -m "Update PWA URLs"
git push azure main
```

---

## 🔍 Monitoring & Logs

### View Live Logs

```powershell
az webapp log tail --name reel-downloader-app --resource-group reel-downloader-rg
```

### Or in Portal:
1. Go to **"Log stream"** in left menu
2. See real-time application logs

### Check App Health:
- Go to **"Diagnose and solve problems"**
- View availability, performance, errors

---

## 💰 Pricing Options

| Tier | Price | Features |
|------|-------|----------|
| **F1 Free** | $0/month | 60 min/day, 1GB storage, custom domain |
| **B1 Basic** | ~$13/month | Always on, 1.75GB RAM, custom domain |
| **S1 Standard** | ~$70/month | Auto-scale, SSL, staging slots |

**Recommendation**: Start with **F1 Free**, upgrade to **B1 Basic** if needed.

### Enable "Always On" (B1+ only)

1. Go to **"Configuration"** → **"General settings"**
2. Set **Always On**: **ON**
3. Prevents app from sleeping

---

## 🔧 Troubleshooting

### App Not Starting

1. Check logs: `az webapp log tail --name reel-downloader-app --resource-group reel-downloader-rg`
2. Verify `startup.txt` exists
3. Check `requirements.txt` has all dependencies

### PWA Not Installing

1. Verify HTTPS is enabled
2. Check `manifest.json` has correct URLs
3. Clear browser cache and try again

### Download Errors

1. Check if `temp_downloads/` folder exists
2. Verify Instaloader is working: check logs
3. Instagram may be rate-limiting: wait and retry

### App Restarts Frequently (Free Tier)

- Free tier sleeps after 20 minutes idle
- Upgrade to B1 Basic and enable "Always On"

---

## 🎉 Post-Deployment Checklist

- [ ] App is accessible via HTTPS
- [ ] PWA installs on mobile
- [ ] Share from Instagram works
- [ ] Background mode shows minimal notification
- [ ] Downloads work correctly
- [ ] Videos are in Downloads folder
- [ ] Old files clean up after 6 hours
- [ ] Custom domain configured (optional)

---

## 📞 Support & Resources

- **Azure Documentation**: https://docs.microsoft.com/azure/app-service/
- **Python on Azure**: https://docs.microsoft.com/azure/developer/python/
- **Pricing Calculator**: https://azure.microsoft.com/pricing/calculator/

---

## 🚀 Quick Deploy Commands (Summary)

```powershell
# Login
az login

# Create resources
az group create --name reel-downloader-rg --location eastus
az appservice plan create --name reel-downloader-plan --resource-group reel-downloader-rg --sku B1 --is-linux
az webapp create --resource-group reel-downloader-rg --plan reel-downloader-plan --name reel-downloader-app --runtime "PYTHON:3.11"

# Configure
az webapp config set --resource-group reel-downloader-rg --name reel-downloader-app --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 --workers=2 app:app"

# Deploy
az webapp deployment source config-local-git --name reel-downloader-app --resource-group reel-downloader-rg
git remote add azure <output_url>
git push azure main

# Done! 🎉
```

---

## 🌐 Your App URLs

After deployment:
- **App URL**: `https://reel-downloader-app.azurewebsites.net`
- **Share Target**: `https://reel-downloader-app.azurewebsites.net/share-target`

**Update `manifest.json` with these URLs before final deployment!**

---

**Your app will now run 24/7 on Azure! 🚀**
