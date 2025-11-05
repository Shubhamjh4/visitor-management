# AWS Free Tier Migration Guide

This guide will help you migrate your Visitor Management System from Render to AWS Free Tier.

---

## AWS Free Tier Options

### Option 1: AWS Elastic Beanstalk (Recommended - Easiest)
**Best for**: Quick deployment, minimal configuration
**Free Tier**: 750 hours/month for 12 months
**Setup Time**: 30-60 minutes

### Option 2: AWS EC2 t2.micro (Most Control)
**Best for**: Full server control, custom configurations
**Free Tier**: 750 hours/month for 12 months
**Setup Time**: 1-2 hours

### Option 3: AWS Lightsail (Simplest)
**Best for**: Beginners, simple deployments
**Cost**: $3.50/month minimum (not free, but very cheap)
**Setup Time**: 30 minutes

---

## Prerequisites

1. **AWS Account**: Sign up at [aws.amazon.com](https://aws.amazon.com)
2. **AWS CLI**: Install from [aws.amazon.com/cli](https://aws.amazon.com/cli)
3. **Git**: Your code should be in a Git repository

---

## Option 1: AWS Elastic Beanstalk Deployment

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize Elastic Beanstalk

```bash
cd visitor_management
eb init
```

Follow the prompts:
- **Select region**: Choose closest to your users (e.g., `us-east-1`)
- **Application name**: `visitor-management`
- **Platform**: Python 3.11 or 3.12
- **Platform version**: Latest
- **SSH**: Yes (recommended)

### Step 3: Create Environment

```bash
eb create visitor-management-env
```

This will:
- Create an EC2 instance
- Set up a load balancer
- Configure security groups
- Deploy your application

### Step 4: Configure Environment Variables

```bash
eb setenv SECRET_KEY='your-secret-key' \
         DEBUG=False \
         ALLOWED_HOSTS='your-app.elasticbeanstalk.com' \
         EMAIL_HOST_USER='your-email' \
         EMAIL_HOST_PASSWORD='your-password' \
         DEFAULT_FROM_EMAIL='your-email' \
         BREVO_API_KEY='your-brevo-key'
```

### Step 5: Set Up PostgreSQL Database

#### Option A: AWS RDS (Free Tier Available)
```bash
# Create RDS instance via AWS Console
# Go to: RDS > Databases > Create database
# Choose: PostgreSQL, Free tier template
# Set database name: visitor_db
# Get connection string and update DATABASE_URL
```

#### Option B: Use Existing Render Database
- Keep using Render database temporarily
- Or migrate to RDS later

### Step 6: Configure Static Files

Create `.ebextensions/01_static.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: visitor_portal/visitor_portal/wsgi:application
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current/visitor_portal:$PYTHONPATH"
```

### Step 7: Deploy

```bash
eb deploy
```

### Step 8: Open Your App

```bash
eb open
```

---

## Option 2: AWS EC2 t2.micro Deployment

### Step 1: Launch EC2 Instance

1. Go to AWS Console > EC2
2. Click "Launch Instance"
3. Configure:
   - **Name**: visitor-management
   - **AMI**: Ubuntu Server 22.04 LTS (Free Tier eligible)
   - **Instance Type**: t2.micro (Free Tier)
   - **Key Pair**: Create new or use existing
   - **Security Group**: Allow HTTP (80), HTTPS (443), SSH (22)

### Step 2: Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Install PostgreSQL client (if needed)
sudo apt install postgresql-client -y

# Install Nginx
sudo apt install nginx -y

# Install Git
sudo apt install git -y
```

### Step 4: Clone Your Repository

```bash
cd /var/www
sudo git clone https://github.com/your-username/visitor-management.git
sudo chown -R ubuntu:ubuntu visitor-management
cd visitor-management
```

### Step 5: Set Up Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 6: Configure Environment Variables

Create `.env` file:
```bash
nano visitor_portal/.env
```

Add:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-ec2-ip-or-domain
DATABASE_URL=your-postgres-url
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=your-email
BREVO_API_KEY=your-brevo-key
```

### Step 7: Run Migrations and Collect Static Files

```bash
cd visitor_portal
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 8: Set Up Gunicorn Service

Create `/etc/systemd/system/visitor-management.service`:
```ini
[Unit]
Description=Visitor Management Gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/visitor-management/visitor_portal
Environment="PATH=/var/www/visitor-management/venv/bin"
ExecStart=/var/www/visitor-management/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/visitor-management/visitor_portal/visitor_portal.sock \
    visitor_portal.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start visitor-management
sudo systemctl enable visitor-management
```

### Step 9: Configure Nginx

Create `/etc/nginx/sites-available/visitor-management`:
```nginx
server {
    listen 80;
    server_name your-domain.com your-ec2-ip;

    location /static/ {
        alias /var/www/visitor-management/visitor_portal/staticfiles/;
    }

    location /media/ {
        alias /var/www/visitor-management/visitor_portal/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/visitor-management/visitor_portal/visitor_portal.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/visitor-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 10: Set Up SSL (Optional but Recommended)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Database Migration

### From Render to AWS RDS

1. **Export data from Render**:
```bash
# On Render, get database connection string
# Export data:
pg_dump $RENDER_DATABASE_URL > backup.sql
```

2. **Create RDS instance**:
- Go to AWS RDS Console
- Create PostgreSQL database (Free tier)
- Get connection string

3. **Import data**:
```bash
psql $AWS_RDS_CONNECTION_STRING < backup.sql
```

4. **Update DATABASE_URL** in your environment variables

---

## Advantages of AWS Over Render

✅ **No Cold Starts**: Services stay active 24/7
✅ **More Control**: Full access to server/configuration
✅ **Better Performance**: Dedicated resources
✅ **Scalability**: Easy to scale up when needed
✅ **Free Tier**: 12 months free (750 hours/month)
✅ **Multiple Services**: Can run multiple apps on same instance

---

## Cost Comparison

| Service | Free Tier | After Free Tier | Cold Starts |
|---------|-----------|-----------------|-------------|
| Render Free | ✅ Unlimited | ❌ N/A (must upgrade) | ❌ Yes |
| AWS EB | ✅ 12 months | ~$29/month | ✅ No |
| AWS EC2 | ✅ 12 months | ~$10/month | ✅ No |
| AWS Lightsail | ❌ $3.50/month | $3.50/month | ✅ No |

---

## Troubleshooting

### Application Not Starting
- Check logs: `eb logs` (Elastic Beanstalk) or `journalctl -u visitor-management` (EC2)
- Verify environment variables are set correctly
- Check database connection

### Static Files Not Loading
- Run `python manage.py collectstatic --noinput`
- Verify Nginx configuration
- Check file permissions

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check security group allows connections
- Ensure database is accessible from EC2 instance

---

## Next Steps After Migration

1. ✅ Update DNS records (if using custom domain)
2. ✅ Test all functionality
3. ✅ Set up automated backups
4. ✅ Configure monitoring (CloudWatch)
5. ✅ Set up CI/CD pipeline

---

## Recommendation

**For beginners**: Use **AWS Elastic Beanstalk** - it's the easiest and handles most configuration automatically.

**For more control**: Use **AWS EC2** - gives you full control but requires more setup.

**For simplicity**: Consider **AWS Lightsail** - $3.50/month but very simple to use.

---

**Last Updated**: 2025
