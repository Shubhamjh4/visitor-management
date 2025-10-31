# 🚀 Free Hosting Deployment Guide

This guide covers deploying your Visitor Management System to **FREE** hosting platforms.

## 📋 Table of Contents

- [Best Free Hosting Options](#best-free-hosting-options)
- [Option 1: Render (Recommended - Easiest)](#option-1-render-recommended---easiest)
- [Option 2: Railway](#option-2-railway)
- [Option 3: Fly.io](#option-3-flyio)
- [Option 4: PythonAnywhere](#option-4-pythonanywhere)
- [Post-Deployment Setup](#post-deployment-setup)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Best Free Hosting Options

### 1. **Render** (⭐ RECOMMENDED - EASIEST)
- ✅ **750 free hours/month** (enough for 24/7 if single service)
- ✅ Free PostgreSQL database
- ✅ Auto SSL certificates
- ✅ GitHub integration
- ✅ Easy setup
- ⚠️ Spins down after 15 min inactivity (takes ~30s to wake)

### 2. **Railway**
- ✅ $5 free credit/month (usually enough for small apps)
- ✅ Excellent developer experience
- ✅ Auto deployments
- ⚠️ Credit-based (not truly unlimited)

### 3. **Fly.io**
- ✅ 3 VMs free
- ✅ Global edge deployment
- ✅ Great for Docker
- ⚠️ Requires more configuration

### 4. **PythonAnywhere**
- ✅ Free tier available
- ✅ Python-focused
- ⚠️ More limited than others

---

## 🎉 Option 1: Render (Recommended - Easiest)

### Step 1: Prepare Your Repository

1. **Push to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/visitor-management.git
   git push -u origin main
   ```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Verify your email

### Step 3: Create PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Set name: `visitor-db`
3. Select **"Free"** plan
4. Choose region closest to you
5. Click **"Create Database"**
6. **Important**: Copy the **"Internal Database URL"** (you'll need it later)

### Step 4: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select your `visitor-management` repo
4. Configure:
   - **Name**: `visitor-management` (or your choice)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && cd visitor_portal && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**:
     ```bash
     cd visitor_portal && gunicorn visitor_portal.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Free

### Step 5: Set Environment Variables

In your Web Service settings → **Environment**, add:

```
SECRET_KEY=your-super-secret-key-here-generate-one
DEBUG=False
DATABASE_URL=<paste-internal-database-url-from-step-3>
ALLOWED_HOSTS=visitor-management.onrender.com,your-custom-domain.com
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your.email@gmail.com
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Gmail App Password:**
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. App Passwords → Generate new app password
4. Copy the 16-character password

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for first deployment
3. Your app will be live at: `https://visitor-management.onrender.com`

### Step 7: Create Superuser

1. In Render dashboard → Your Web Service → **"Shell"**
2. Run:
   ```bash
   cd visitor_portal
   python manage.py createsuperuser
   ```
3. Follow prompts to create admin user

### Step 8: Import Employees (Optional)

In the Shell:
```bash
cd visitor_portal
python manage.py import_employees visitors/data/employees.csv
```

---

## 🚂 Option 2: Railway

### Step 1: Push to GitHub

Same as Render Step 1

### Step 2: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**

### Step 3: Add PostgreSQL

1. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Wait for database to provision

### Step 4: Configure Service

1. Railway auto-detects Django
2. If not, set:
   - **Root Directory**: Leave empty
   - **Command**: 
     ```bash
     cd visitor_portal && gunicorn visitor_portal.wsgi:application --bind 0.0.0.0:$PORT
     ```

### Step 5: Set Environment Variables

In your service → **Variables**, add:

```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=${{Postgres.DATABASE_URL}}
ALLOWED_HOSTS=*.railway.app,your-domain.com
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your.email@gmail.com
```

### Step 6: Deploy & Setup

1. Railway auto-deploys on push
2. Create superuser via Railway CLI or deploy logs terminal
3. Import employees (same commands as Render)

---

## ✈️ Option 3: Fly.io

### Step 1: Install Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Or download from: https://fly.io/docs/getting-started/installing-flyctl/
```

### Step 2: Create Fly Account

```bash
fly auth signup
```

### Step 3: Initialize Fly App

```bash
cd visitor_management
fly launch
```

Follow prompts:
- App name: `visitor-management` (or auto-generated)
- Region: Choose closest
- PostgreSQL: Yes (free tier)
- Redis: No

### Step 4: Set Secrets

```bash
fly secrets set SECRET_KEY="your-secret-key"
fly secrets set DEBUG="False"
fly secrets set ALLOWED_HOSTS="visitor-management.fly.dev,your-domain.com"
fly secrets set EMAIL_HOST_USER="your.email@gmail.com"
fly secrets set EMAIL_HOST_PASSWORD="your-app-password"
fly secrets set DEFAULT_FROM_EMAIL="your.email@gmail.com"
```

### Step 5: Deploy

```bash
fly deploy
```

### Step 6: Create Superuser

```bash
fly ssh console
cd visitor_portal
python manage.py createsuperuser
```

---

## 🐍 Option 4: PythonAnywhere

### Step 1: Create Account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up (free "Beginner" account)

### Step 2: Upload Your Code

1. **Files** tab → Upload project ZIP
2. Or use Git:
   ```bash
   git clone https://github.com/YOUR_USERNAME/visitor-management.git
   ```

### Step 3: Create Web App

1. **Web** tab → **"Add a new web app"**
2. Choose domain (free: `username.pythonanywhere.com`)
3. Select **"Manual configuration"** → **Python 3.10**

### Step 4: Configure WSGI

1. In **Web** tab → **WSGI configuration file**
2. Edit and set:
   ```python
   import sys
   import os
   
   path = '/home/YOUR_USERNAME/visitor-management/visitor_portal'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'visitor_portal.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

### Step 5: Set Environment Variables

In **Web** tab → **Environment variables**:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=username.pythonanywhere.com
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Step 6: Setup Database

Free tier uses SQLite (already configured). For PostgreSQL, upgrade.

### Step 7: Run Migrations

**Bash console**:
```bash
cd ~/visitor-management/visitor_portal
python3.10 manage.py migrate
python3.10 manage.py createsuperuser
python3.10 manage.py collectstatic
```

### Step 8: Reload Web App

Click **"Reload"** button in Web tab

---

## 🔧 Post-Deployment Setup

### For All Platforms:

1. **Create Admin User**:
   ```bash
   python manage.py createsuperuser
   ```

2. **Import Employees**:
   ```bash
   python manage.py import_employees visitors/data/employees.csv
   ```

3. **Verify Static Files**:
   - Check if CSS/JS loads correctly
   - Run `collectstatic` if needed

4. **Test Email**:
   - Try visitor check-in
   - Verify OTP email is received

5. **Set Up Custom Domain** (Optional):
   - In platform settings → Add custom domain
   - Update DNS records as instructed
   - Update `ALLOWED_HOSTS` environment variable

---

## 🔍 Troubleshooting

### App Won't Start

**Check:**
- All environment variables set correctly
- `SECRET_KEY` is set
- `DATABASE_URL` is correct (for PostgreSQL)
- `ALLOWED_HOSTS` includes your domain
- Build logs for errors

### Static Files Not Loading

**Solution:**
```bash
cd visitor_portal
python manage.py collectstatic --noinput
```

### Database Errors

**For PostgreSQL:**
- Verify `DATABASE_URL` is correct
- Check database is running (Render/Railway)
- Run migrations: `python manage.py migrate`

**For SQLite:**
- Ensure write permissions on project directory
- Check `db.sqlite3` exists

### Email Not Sending

**Check:**
- `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are correct
- Using Gmail App Password (not regular password)
- SMTP port 587 is allowed (should be on all platforms)

### 500 Internal Server Error

**Debug Steps:**
1. Temporarily set `DEBUG=True` to see error
2. Check logs in platform dashboard
3. Verify all environment variables are set
4. Check database connection

### Slow Cold Starts (Render Free Tier)

- App spins down after 15 min inactivity
- First request takes ~30 seconds
- Consider upgrading to paid tier for always-on

---

## 📊 Comparison Table

| Platform | Free Tier | Database | Easy Setup | Always On | Best For |
|----------|-----------|----------|------------|-----------|----------|
| **Render** | ⭐⭐⭐⭐⭐ | ✅ PostgreSQL | ⭐⭐⭐⭐⭐ | ⚠️ 15min timeout | **Beginners** |
| **Railway** | ⭐⭐⭐⭐ | ✅ PostgreSQL | ⭐⭐⭐⭐⭐ | ✅ Yes | Quick deploys |
| **Fly.io** | ⭐⭐⭐ | ✅ PostgreSQL | ⭐⭐⭐ | ✅ Yes | Docker fans |
| **PythonAnywhere** | ⭐⭐⭐ | ⚠️ SQLite only | ⭐⭐⭐ | ✅ Yes | Python-focused |

---

## 🎯 Recommendation

**For your small business application, I recommend Render because:**
- ✅ Easiest setup
- ✅ Free PostgreSQL included
- ✅ Auto SSL
- ✅ GitHub integration
- ✅ Good documentation
- ✅ Reliable for low traffic

Start with **Render**, and if you need always-on or more resources later, consider Railway or upgrading Render.

---

## 📝 Next Steps After Deployment

1. ✅ Test visitor check-in flow
2. ✅ Verify email notifications work
3. ✅ Set up employee CSV import
4. ✅ Create admin user
5. ✅ Test guard dashboard
6. ✅ Monitor logs for errors
7. ✅ Set up custom domain (optional)
8. ✅ Configure backups (if available on platform)

---

**Need Help?** Check platform-specific docs:
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Fly.io Docs](https://fly.io/docs)
- [PythonAnywhere Docs](https://help.pythonanywhere.com)

---

**Good luck with your deployment! 🚀**

