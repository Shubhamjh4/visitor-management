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

**What is this?** The PostgreSQL database stores all your app data:
- ✅ Employees (names, departments, emails)
- ✅ Visitors (visitor information, photos)
- ✅ Visit records (check-in/check-out times, history)
- ✅ User accounts (admin/logins)

**About the Free Tier Expiration Warning:**
- ⚠️ Render's **free PostgreSQL expires after 90 days**
- This is normal for free tiers (to prevent abuse)
- **Options:**
  1. **Use it for now** - You have ~90 days free (good for testing)
  2. **Upgrade later** - Only $7/month when you need permanent storage
  3. **Use external free DB** - See alternative below for truly free options

**Steps:**
1. Click **"New +"** → **"PostgreSQL"**
2. Name: `visitor-db`
3. Plan: **Free** (click continue despite expiration warning)
4. Create
5. Copy **"Internal Database URL"** ⚠️ (you'll need this in Step 5)

**💡 Alternative: Use Neon (Truly Free Database - No Expiration!)**

If you want a database that **never expires** (free forever), use Neon instead:

**Why Neon?**
- ✅ Completely free forever (no expiration!)
- ✅ 0.5 GB storage (enough for thousands of visitors)
- ✅ Works perfectly with Render
- ✅ Easy to set up (just a few steps)

**Step-by-Step Setup (Beginner Friendly):**

1. **Go to Neon Website**
   - Open your browser
   - Visit: [neon.tech](https://neon.tech)
   - Click the **"Sign Up"** or **"Get Started"** button

2. **Create Your Account**
   - Sign up with **Google** (easiest) or email
   - Verify your email if needed

3. **Create a New Project**
   - After logging in, you'll see a dashboard
   - Click the big **"Create Project"** button
   - Enter project name: `visitor-management` (or any name you like)
   - Select region: Choose closest to you (e.g., "US East" or "EU West")
   - Click **"Create Project"**
   - Wait 1-2 minutes for setup to complete

4. **Find Your Connection String**
   - After project is created, you'll see a page with connection details
   - Look for **"Connection string"** or **"Database URL"**
   - You'll see something like:
     ```
     postgres://username:password@ep-xxxx-xxxx.us-east-2.aws.neon.tech/neondb
     ```
   - There's usually a **"Copy"** button next to it - click it!
   - ⚠️ **SAVE THIS SOMEWHERE** (notepad, notes app, etc.) - You'll need it in Step 5!

5. **Skip Render Database Step**
   - **Don't create a database in Render** (skip Step 3 above)
   - You're using Neon instead, so Render database is not needed

6. **Use Neon in Render** (Go to Step 5 below)
   - When you reach **Step 5: Set Environment Variables**
   - Instead of Render's database URL, paste Neon's connection string
   - Everything else works exactly the same!

**That's it!** Neon is now your database, and it's free forever! 🎉

**Need help?** Neon's interface is very user-friendly. If you get stuck:
- Look for the "Connection string" or "Database URL" section
- It's usually on the main project page or in "Settings"
- The connection string starts with `postgres://`

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

**What are these?** These are secret settings your app needs to work. Think of them as passwords and configuration.

1. In your Web Service page, scroll down or look for **"Environment"** tab/section
2. Click **"Add Environment Variable"** button (might be labeled as "Add" or "+")
3. Add each variable one by one (click "Add" after each):

   **Variable 1: SECRET_KEY** (Important: Django needs this!)
   - **Key**: `SECRET_KEY`
   - **Value**: Generate one first:
     - Open Command Prompt or PowerShell on your computer
     - Type this command and press Enter:
       ```bash
       python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
       ```
     - Copy the long random string it shows (starts with something like `django-insecure-...`)
     - Paste this entire string as the value
   - This is like a master password for your app - keep it secret!

   **Variable 2: DEBUG**
   - **Key**: `DEBUG`
   - **Value**: `False`

   **Variable 3: DATABASE_URL**
   - **Key**: `DATABASE_URL`
   - **Value**: 
     - If using **Render database**: Paste the "Internal Database URL" from Step 3
     - If using **Neon database**: Paste the Neon connection string you copied (from Step 3 alternative)

   **Variable 4: ALLOWED_HOSTS**
   - **Key**: `ALLOWED_HOSTS`
   - **Value**: `visitor-management.onrender.com` (or your actual Render URL)

   **Variable 5: EMAIL_HOST_USER**
   - **Key**: `EMAIL_HOST_USER`
   - **Value**: Your Gmail address (e.g., `your.email@gmail.com`)

   **Variable 6: EMAIL_HOST_PASSWORD**
   - **Key**: `EMAIL_HOST_PASSWORD`
   - **Value**: Your Gmail App Password (16 characters, see how to get it below)

   **Variable 7: DEFAULT_FROM_EMAIL**
   - **Key**: `DEFAULT_FROM_EMAIL`
   - **Value**: Same as EMAIL_HOST_USER (your Gmail address)

**How to Get Gmail App Password:**
1. Go to your Google Account → Security
2. Enable "2-Step Verification" (if not already enabled)
3. Go to "App passwords" (search for it)
4. Select "Mail" and your device
5. Click "Generate"
6. Copy the 16-character password (no spaces)
7. Use this in `EMAIL_HOST_PASSWORD` above

**After adding all variables**, your list should show 7 items. ✅

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

