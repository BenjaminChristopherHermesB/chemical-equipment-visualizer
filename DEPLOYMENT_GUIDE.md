# DEPLOYMENT & USAGE INSTRUCTIONS

## 🎯 Quick Start - For You

This document provides **exact, step-by-step instructions** tailored to your deployed system.

---

## STEP 1: Initialize Git and Push to GitHub

```powershell
cd "C:\Users\Benjamin B C H\OneDrive\Documents\B.E\BenjaminsPrograms\Python\Internship\chemical-equipment-visualizer"

git init
git add .
git commit -m "Complete hybrid Chemical Equipment Visualizer application"
git branch -M main
git remote add origin https://github.com/BenjaminChristopherHermesB/chemical-equipment-visualizer.git
git push -u origin main
```

---

## STEP 2: Deploy Django Backend to Render

### 2.1: Create Render Account
- Go to https://render.com
- Sign up with GitHub (recommended)

### 2.2: Create PostgreSQL Database (Optional but Recommended)
1. Click "New +" → "PostgreSQL"
2. Name: `chemical-equipment-db`
3. Database: `equipment_db`
4. User: `equipment_user`
5. Region: Choose closest to you
6. Instance Type: **Free**
7. Click "Create Database"
8. **SAVE** the "Internal Database URL" - you'll need this

### 2.3: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `chemical-equipment-visualizer`
3. Configure:
   - **Name**: `chemical-equipment-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn equipment_visualizer.wsgi:application --bind 0.0.0.0:$PORT`
   - **Instance Type**: **Free**

### 2.4: Add Environment Variables
Click "Environment" → "Add Environment Variable" and add these:

```
DEBUG=False
SECRET_KEY=django-insecure-p7k9m2n5q8r3t6v9w2x5z8a3c6e9g2j5m8p1r4t7v0y3b6d9
ALLOWED_HOSTS=.onrender.com
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://*.vercel.app
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
DATABASE_URL=<paste-database-url-from-step-2.2-if-using-postgres>
```

### 2.5: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for first deployment
3. **SAVE YOUR BACKEND URL**: `https://chemical-equipment-backend.onrender.com`

### 2.6: Create Superuser (Optional - For Admin Panel)
1. Go to your service in Render dashboard
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow prompts to create admin user
5. Access admin at: `https://chemical-equipment-backend.onrender.com/admin/`

---

## STEP 3: Deploy React Web Frontend to Vercel

### 3.1: Create Vercel Account
- Go to https://vercel.com
- Sign up with GitHub

### 3.2: Import Project
1. Click "Add New..." → "Project"
2. Import `chemical-equipment-visualizer` repository
3. Configure:
   - **Framework**: Vite (auto-detected)
   - **Root Directory**: `frontend-web`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 3.3: Add Environment Variable
Click "Environment Variables" and add:

```
VITE_API_BASE_URL=https://chemical-equipment-backend.onrender.com/api
```

### 3.4: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes
3. **SAVE YOUR WEB APP URL**: `https://chemical-equipment-visualizer.vercel.app`

### 3.5: Update Backend CORS
1. Go back to Render dashboard
2. Go to your backend service
3. Update `CORS_ALLOWED_ORIGINS` environment variable:
   ```
   CORS_ALLOWED_ORIGINS=https://chemical-equipment-visualizer.vercel.app
   ```
4. Service will auto-redeploy

---

## STEP 4: Package Desktop App

### 4.1: Install Dependencies
```powershell
cd "C:\Users\Benjamin B C H\OneDrive\Documents\B.E\BenjaminsPrograms\Python\Internship\chemical-equipment-visualizer\frontend-desktop"

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4.2: Build Executable
```powershell
pyinstaller ChemicalEquipmentVisualizer.spec
```

### 4.3: Test Executable
```powershell
.\dist\ChemicalEquipmentVisualizer.exe
```

- When prompted for API URL, enter: `https://chemical-equipment-backend.onrender.com/api`

---

## STEP 5: Test Complete System

### 5.1: Test Web App
1. Go to `https://chemical-equipment-visualizer.vercel.app`
2. Click "Register" tab
3. Create account: `testuser` / `TestPass123!`
4. Should auto-login
5. Upload `file.csv` from your repository
6. Verify:
   - ✅ Charts appear
   - ✅ Statistics calculated
   - ✅ Data table populated
   - ✅ PDF downloads
7. Check "History" tab - dataset appears

### 5.2: Test Desktop App
1. Launch `ChemicalEquipmentVisualizer.exe`
2. Enter API URL: `https://chemical-equipment-backend.onrender.com/api`
3. Login with same credentials
4. Check "History" tab - web upload appears ✅
5. Upload another CSV from desktop
6. Go back to web app - new upload appears in history ✅

---

## ACCESSING YOUR DEPLOYED SYSTEM

### Backend API
- **URL**: `https://chemical-equipment-backend.onrender.com`
- **API Base**: `https://chemical-equipment-backend.onrender.com/api/`
- **Admin Panel**: `https://chemical-equipment-backend.onrender.com/admin/`
- **Health Check**: `https://chemical-equipment-backend.onrender.com/api/health/`

### Web Frontend
- **URL**: `https://chemical-equipment-visualizer.vercel.app`

### Desktop App
- **Location**: `C:\Users\Benjamin B C H\OneDrive\Documents\B.E\BenjaminsPrograms\Python\Internship\chemical-equipment-visualizer\frontend-desktop\dist\ChemicalEquipmentVisualizer.exe`
- **API URL** (when prompted): `https://chemical-equipment-backend.onrender.com/api`

---

## HOW TO USE THE SYSTEM

### Web App Workflow

1. **Go to**: `https://chemical-equipment-visualizer.vercel.app`
2. **Register**: Enter username, password, confirm password
3. **Upload CSV**:
   - Stay on "Upload CSV" tab
   - Drag `file.csv` or click to browse
   - Click "Upload and Process"
4. **View Results**:
   - Auto-redirects to "Visualization" tab
   - See statistics cards, data table, 4 charts
5. **Download PDF**: Click "Download PDF Report"
6. **View History**: Click "History" tab → see last 5 uploads

### Desktop App Workflow

1. **Launch**: `ChemicalEquipmentVisualizer.exe`
2. **Enter API URL**: `https://chemical-equipment-backend.onrender.com/api`
3. **Login**: Use web credentials OR register new account
4. **Upload CSV**:
   - "Upload CSV" tab
   - "Choose CSV File" button
   - Select `file.csv`
5. **View Results**:
   - Auto-switches to "Visualization" tab
   - See statistics, table, charts
6. **Download PDF**: "Download PDF Report" → Choose location
7. **View History**: "History" tab → Double-click to reload dataset

---

## DEMO VIDEO SCRIPT (2-3 Minutes)

### Scene 1: Introduction (20s)
- Show project folder structure
- "Built a hybrid application with 3 components..."
- Show README quickly

### Scene 2: Web App (60s)
1. Open browser to Vercel URL
2. Register new account
3. Drag-and-drop CSV upload
4. Show all 4 charts appearing
5. Show summary statistics
6. Click "Download PDF" - open PDF
7. Show History tab

### Scene 3: Desktop App (60s)
1. Launch executable
2. Enter API URL
3. Login
4. Upload CSV
5. Show Matplotlib charts
6. Download PDF
7. Show History - double-click to reload

### Scene 4: Backend (20s)
- Open Django admin panel
- Show EquipmentDataset entries
- Show only 5 datasets stored per user

---

## CREDENTIALS & LINKS SUMMARY

**GitHub Repository**:
```
https://github.com/BenjaminChristopherHermesB/chemical-equipment-visualizer
```

**Backend (Render)**:
```
URL: https://chemical-equipment-backend.onrender.com
API: https://chemical-equipment-backend.onrender.com/api/
Admin: https://chemical-equipment-backend.onrender.com/admin/
```

**Frontend (Vercel)**:
```
URL: https://chemical-equipment-visualizer.vercel.app
```

**Desktop App**:
```
Path: C:\Users\Benjamin B C H\...\frontend-desktop\dist\ChemicalEquipmentVisualizer.exe
API URL: https://chemical-equipment-backend.onrender.com/api
```

**Sample Data**:
```
File: file.csv (in repository root or Internship folder)
```

---

## TROUBLESHOOTING

### "Backend not responding"
- Render free tier sleeps after 15 min inactivity
- First request takes 30-60s to wake up
- Refresh and wait

### "CORS error"
- Check Render environment variable `CORS_ALLOWED_ORIGINS` includes your Vercel URL
- Redeploy backend if you changed it

### "Desktop app can't connect"
- Verify API URL is exactly: `https://chemical-equipment-backend.onrender.com/api`
- No trailing slash!

### "Charts not showing"
- Web: Hard refresh (Ctrl+Shift+R)
- Desktop: Close and reopen

---

## SUCCESS CRITERIA ✅

- ✅ Backend deployed and accessible
- ✅ Web app deployed and accessible
- ✅ Desktop app packaged as .exe
- ✅ All three components communicate via same API
- ✅ CSV upload works from both frontends
- ✅ Statistics computed correctly
- ✅ Charts render in both frontends
- ✅ PDF generation works
- ✅ History shows last 5 datasets
- ✅ Authentication works across platforms
- ✅ Demo video recorded

---

**YOU'RE ALL SET!** 🎉

Everything is built. Now just:
1. Push to GitHub
2. Deploy to Render (backend)
3. Deploy to Vercel (frontend)
4. Package desktop app
5. Record demo video

All code is complete and ready to deploy!
