# 🗄️ Database Options for Free Hosting

## Quick Answer

**The PostgreSQL database stores:**
- ✅ Employee data (names, departments, emails, phone numbers)
- ✅ Visitor information (names, emails, addresses, photos)
- ✅ Visit records (check-in/check-out times, visit history)
- ✅ User accounts (admin users, passwords)

**Without a database, your app can't store or retrieve any data!**

---

## 🆓 Free Database Options

### Option 1: Render PostgreSQL (Easiest)
**Pros:**
- ✅ Super easy setup (built into Render)
- ✅ Free for 90 days
- ✅ No external setup needed

**Cons:**
- ⚠️ **Expires after 90 days** (November 30, 2025 in your case)
- ⚠️ Need to upgrade ($7/month) or migrate data later

**Best for:** Testing, learning, short-term projects

**How to use:**
1. Follow Step 3 in QUICK_START_DEPLOY.md
2. Accept the expiration warning (it's fine for testing)
3. You can always export data and migrate later

---

### Option 2: Neon (Recommended for Permanent Free)
**Pros:**
- ✅ **Free forever** (no expiration)
- ✅ 0.5 GB storage free
- ✅ Good for small businesses
- ✅ Easy connection to Render

**Cons:**
- ⚠️ Need separate signup
- ⚠️ Slightly more setup

**Best for:** Production apps, long-term projects

**Setup Steps:**
1. Go to [neon.tech](https://neon.tech) and sign up (free)
2. Click "Create Project"
3. Name it `visitor-management`
4. Copy the connection string (looks like: `postgres://user:pass@host/dbname`)
5. In Render → Web Service → Environment Variables:
   - Set `DATABASE_URL` to Neon's connection string
6. Skip Render database creation

**Free tier limits:**
- 0.5 GB storage
- Unlimited projects
- Auto-pause after inactivity (wakes automatically)

---

### Option 3: Supabase (Alternative Free Option)
**Pros:**
- ✅ Free forever
- ✅ 500 MB database
- ✅ Includes other features (auth, storage)

**Cons:**
- ⚠️ More complex setup

**Setup:**
1. Sign up at [supabase.com](https://supabase.com)
2. Create project
3. Go to Settings → Database
4. Copy connection string
5. Use in Render environment variables

---

### Option 4: Railway PostgreSQL
**Pros:**
- ✅ $5 free credit/month (usually covers small DB)
- ✅ Easy setup if using Railway for hosting

**Cons:**
- ⚠️ Credit-based (not unlimited)
- ⚠️ Need Railway account

---

## 📊 Comparison Table

| Provider | Cost | Storage | Expires? | Easiest? |
|----------|------|---------|----------|----------|
| **Render** | Free | 90 days | ⚠️ Yes (90 days) | ⭐⭐⭐⭐⭐ |
| **Neon** | Free | 0.5 GB | ✅ No | ⭐⭐⭐⭐ |
| **Supabase** | Free | 500 MB | ✅ No | ⭐⭐⭐ |
| **Railway** | $5 credit | Varies | ✅ No | ⭐⭐⭐ |

---

## 💡 My Recommendation

### For Testing/Learning (First 90 Days):
**Use Render PostgreSQL** - Easiest setup, perfect for testing your app

### For Production (Long-term):
**Use Neon** - Free forever, easy migration, no expiration worries

---

## 🔄 Migrating from Render to Neon (When Needed)

When your Render database expires, you can migrate:

### Step 1: Export Data from Render
In Render → Shell:
```bash
cd visitor_portal
python manage.py dumpdata --exclude=contenttypes --exclude=auth.permission --natural-foreign --natural-primary --indent 2 > backup.json
```

### Step 2: Set Up Neon
1. Create Neon account
2. Create database
3. Copy connection string

### Step 3: Update Render
In Render → Environment Variables:
- Update `DATABASE_URL` to Neon's connection string

### Step 4: Import Data
In Render → Shell:
```bash
cd visitor_portal
python manage.py migrate
python manage.py loaddata backup.json
```

**Done!** Your data is now in Neon (free forever).

---

## ❓ FAQ

### Q: What happens when Render database expires?
**A:** Your database gets deleted. Export your data before expiration and migrate to Neon/Supabase.

### Q: Can I use SQLite instead?
**A:** Not recommended on Render free tier. Render's disk is ephemeral (wipes on restart), so you'll lose data.

### Q: How much data can I store?
**A:** 
- Render free: Small projects (~100MB)
- Neon free: 0.5 GB (thousands of visitors)
- Supabase free: 500 MB

### Q: Will I lose data if I switch databases?
**A:** No! Use `dumpdata`/`loaddata` to export/import. Your data moves with you.

---

## ✅ Quick Decision Guide

**Choose Render PostgreSQL if:**
- ✅ You're just testing/learning
- ✅ You want the easiest setup
- ✅ You're okay migrating in 90 days

**Choose Neon if:**
- ✅ You want permanent free database
- ✅ This is for real business use
- ✅ You want no expiration worries

**Both work perfectly!** Choose based on your needs. 🚀

