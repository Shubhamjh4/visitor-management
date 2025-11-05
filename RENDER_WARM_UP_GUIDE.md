# Render Free Tier Warm-Up Solution

## Problem
Render's free tier services spin down after ~15 minutes of inactivity, causing cold starts (30-60 seconds) when users access the app after inactivity.

## Solution: Free Health Check Service

Use a free uptime monitoring service to ping your app every 14 minutes, keeping it warm and preventing spin-down.

---

## Option 1: UptimeRobot (Recommended - Free)

### Step 1: Sign Up for UptimeRobot
1. Go to [https://uptimerobot.com/](https://uptimerobot.com/)
2. Sign up for a free account (supports up to 50 monitors)

### Step 2: Add a Monitor
1. Log in to UptimeRobot dashboard
2. Click **"Add New Monitor"**
3. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Visitor Management Warm-Up
   - **URL**: `https://visitor-management.onrender.com/health/`
   - **Monitoring Interval**: 5 minutes (minimum for free tier)
   - **Alert Contacts**: (Optional) Add your email if you want notifications

4. Click **"Create Monitor"**

### Step 3: Verify It's Working
- Wait 5-10 minutes
- Check your Render dashboard - the service should stay active
- Test accessing your app - it should load instantly without cold start

**Note**: Free tier allows 5-minute intervals (not 14 minutes), but this is still effective at keeping your service warm.

---

## Option 2: cron-job.org (Free) ✅ **Recommended for Commercial Use**

### Step 1: Sign Up
1. Go to [https://cron-job.org/](https://cron-job.org/)
2. Sign up for a free account

### Step 2: Create Cron Job
1. After logging in, click **"Create cronjob"**
2. Configure:
   - **Title**: Render Warm-Up
   - **Address**: `https://visitor-management.onrender.com/health/`
   - **Schedule**: Every 14 minutes (or use cron expression: `*/14 * * * *`)
   - **Notifications**: (Optional) Enable if you want alerts

3. Click **"Create cronjob"**

### ✅ Can I Use Both UptimeRobot AND cron-job.org?

**Yes, absolutely!** Using both services together is actually beneficial:

✅ **Redundancy**: If one service goes down, the other keeps your app warm
✅ **No Conflicts**: Both services just ping your endpoint - they don't interfere with each other
✅ **More Frequent Pings**: Combined intervals mean your app gets pinged more often
✅ **Free**: Both are free to use

**Example Timeline:**
- UptimeRobot: Pings every 5 minutes (at 0:00, 0:05, 0:10, 0:15...)
- cron-job.org: Pings every 14 minutes (at 0:00, 0:14, 0:28, 0:42...)
- Result: Your app gets pinged roughly every 3-5 minutes, keeping it very warm!

**Note**: The health check endpoint is lightweight (no database queries), so multiple pings won't cause any performance issues.

---

## Option 3: PythonAnywhere Free Scheduler

If you have a PythonAnywhere account, you can use their free scheduler:
1. Create a simple Python script that makes HTTP requests
2. Schedule it to run every 14 minutes

---

## Alternative: AWS Free Tier Migration

If you prefer to migrate to AWS, here are the options:

### AWS Options:

#### 1. **AWS Elastic Beanstalk** (Easiest)
- Free tier: 750 hours/month for 12 months
- No cold starts
- Easy deployment similar to Render

#### 2. **AWS EC2 t2.micro** (Most Control)
- Free tier: 750 hours/month for 12 months
- Full control over server
- No cold starts
- Requires more setup

#### 3. **AWS Lightsail** (Simplest for Beginners)
- $3.50/month minimum (not free, but very cheap)
- Simple deployment
- No cold starts

---

## Current Setup

Your app now has a health check endpoint at: `/health/`

This endpoint:
- ✅ Returns a simple JSON response
- ✅ Does not hit the database (fast and lightweight)
- ✅ Perfect for monitoring services
- ✅ Won't affect your app's performance

---

## Testing the Health Check

Test locally:
```bash
cd visitor_portal
python manage.py runserver
# Visit: http://127.0.0.1:8000/health/
```

Test on Render:
```bash
# Visit: https://visitor-management.onrender.com/health/
# Should return: {"status": "ok", "service": "visitor-management"}
```

---

## Monitoring Multiple Services

If you have multiple Render services, you can:
1. Add multiple monitors in UptimeRobot (free tier supports 50)
2. Use the same health check endpoint for all
3. Configure different intervals if needed

---

## Troubleshooting

### Service Still Spinning Down?
- Check that the monitoring service is actually running
- Verify the URL is correct (should end with `/health/`)
- Check Render logs to see if requests are coming through
- Ensure monitoring interval is less than 15 minutes

### Health Check Not Working?
- Verify the endpoint is accessible: `https://your-app.onrender.com/health/`
- Check Render deployment logs for errors
- Ensure the deployment was successful after adding the health check

---

## Cost Comparison

| Solution | Cost | Cold Starts | Setup Time |
|----------|------|-------------|------------|
| Render + UptimeRobot | Free | None | 5 minutes |
| Render + cron-job.org | Free | None | 5 minutes |
| AWS Elastic Beanstalk | Free (12 months) | None | 30-60 minutes |
| AWS EC2 | Free (12 months) | None | 1-2 hours |
| AWS Lightsail | $3.50/month | None | 30 minutes |

---

## Recommendation

**For immediate solution**: Use UptimeRobot (Option 1) - it's free, takes 5 minutes to set up, and solves your problem immediately.

**For long-term**: If you want more control and don't mind AWS setup, migrate to AWS Elastic Beanstalk or EC2 free tier.

---

## Next Steps

1. ✅ Health check endpoint is already added to your app
2. Deploy the changes to Render (if not already deployed)
3. Set up UptimeRobot or cron-job.org
4. Test that your app loads instantly after inactivity

---

**Last Updated**: 2025
