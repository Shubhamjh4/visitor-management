# 🚀 Quick Start: Deploy to Render (FREE)

**Fastest way to get your app online - 10 minutes!**

## Step-by-Step

### 1. Push Code to GitHub
```bash
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/visitor-management.git
git push -u origin main
```

### 2. Sign Up for Render
- Go to [render.com](https://render.com)
- Sign up with GitHub
- Verify email

### 3. Create Database
1. Click **"New +"** → **"PostgreSQL"**
2. Name: `visitor-db`
3. Plan: **Free**
4. Create
5. Copy **"Internal Database URL"** ⚠️

### 4. Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub → Select your repo
3. Settings:
   - **Name**: `visitor-management`
   - **Plan**: Free
   - **Build Command**:
     ```
     pip install -r requirements.txt && cd visitor_portal && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**:
     ```
     cd visitor_portal && gunicorn visitor_portal.wsgi:application --bind 0.0.0.0:$PORT
     ```

### 5. Set Environment Variables
In Web Service → **Environment**, add:

```
SECRET_KEY=<generate-using-command-below>
DEBUG=False
DATABASE_URL=<paste-internal-db-url-from-step-3>
ALLOWED_HOSTS=visitor-management.onrender.com
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your.email@gmail.com
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Deploy!
Click **"Create Web Service"** and wait 5-10 minutes.

### 7. Create Admin User
1. Web Service → **Shell** tab
2. Run:
   ```bash
   cd visitor_portal
   python manage.py createsuperuser
   ```

### 8. Import Employees (Optional)
```bash
python manage.py import_employees visitors/data/employees.csv
```

## ✅ Done!

Your app is live at: `https://visitor-management.onrender.com`

---

**Need more details?** See [DEPLOYMENT.md](DEPLOYMENT.md)

**Problems?** Check logs in Render dashboard → Logs tab

