# 🚀 Quick Commands: Push to GitHub

## Simple Answer

**Push MOST files, but NOT:**
- ❌ `db.sqlite3` (your database)
- ❌ `media/` folders (visitor photos)
- ❌ `.env` file (passwords)

**✅ Everything else is safe to push!**

---

## Quick Commands

### First Time Setup

```bash
# 1. Go to project folder
cd visitor_management

# 2. Initialize git (if not done)
git init

# 3. Check what will be pushed (IMPORTANT!)
git status
```

**⚠️ Verify these are NOT in the list:**
- `db.sqlite3`
- `.env`
- `visitor_portal/media/`
- `media/`

### If Everything Looks Safe, Continue:

```bash
# 4. Add all safe files
git add .

# 5. Commit
git commit -m "Ready for deployment"

# 6. Connect to GitHub (create repo on GitHub first!)
git remote add origin https://github.com/YOUR_USERNAME/visitor-management.git
git branch -M main

# 7. Push!
git push -u origin main
```

---

## What Gets Pushed?

### ✅ YES - These files will be pushed:
- All Python code (`.py` files)
- Templates (`.html` files)
- CSS/JS files
- `requirements.txt`
- `Procfile`, `Dockerfile`
- `render.yaml`, `railway.json`
- All deployment files
- Documentation (`.md` files)
- Employee CSV (if not sensitive)

### ❌ NO - These are excluded by `.gitignore`:
- `db.sqlite3` ← Your database (NOT pushed)
- `visitor_portal/media/` ← Visitor photos (NOT pushed)
- `.env` ← Passwords (NOT pushed)
- `__pycache__/` ← Python cache (NOT pushed)
- `venv/` ← Virtual environment (NOT pushed)

---

## Quick Check Before Push

Run this to see what WILL be pushed:
```bash
git status
```

**Safe to push if you see:**
- ✅ `.py` files
- ✅ `.html` files
- ✅ `.md` files
- ✅ `requirements.txt`
- ✅ Deployment configs

**DANGER if you see:**
- ❌ `db.sqlite3` → Remove: `git rm --cached visitor_portal/db.sqlite3`
- ❌ `.env` → Remove: `git rm --cached .env`
- ❌ `visitor_portal/media/` → Already excluded by `.gitignore`

---

## That's It! 

Your `.gitignore` file protects you automatically. Just run:
```bash
git add .
git commit -m "Initial commit"
git push
```

**The sensitive files won't be pushed because they're in `.gitignore`!** ✅

---

**Need more details?** See [GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md)

