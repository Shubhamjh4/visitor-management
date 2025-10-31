# Visitor Management System

A comprehensive visitor management system built with Django that allows businesses to track visitors, send email notifications, and manage employee visits with OTP email verification.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Managing Employees](#managing-employees)
- [Email Setup](#email-setup)
- [Development](#development)
- [Production Deployment](#production-deployment)

## ✨ Features

### Visitor Management
- **Visitor Check-in Form** - Modern, mobile-friendly intake form with employee autocomplete
- **Email-based OTP Verification** - Secure 6-digit verification code sent to visitor's email
- **Visit Tracking** - Real-time visit duration tracking with automatic timer
- **Session Management** - Multiple visits supported with session tracking
- **Visitor History** - Complete history of all visits stored in database

### Employee Management
- **CSV Import System** - Bulk import employees from CSV file
- **Autocomplete Search** - Smart employee search with department filtering
- **Email Notifications** - Employees receive email notifications when visitors arrive
- **Active/Inactive Status** - Manage employee availability

### Dashboard & Admin
- **Guard Dashboard** - Monitor ongoing and recent visits with search and filters
- **Real-time Updates** - AJAX-powered updates without page refresh
- **Admin Panel** - Full Django admin integration for advanced management
- **Search & Filters** - Search by visitor name, phone, employee, department, or purpose
- **Month Filter** - Filter visits by specific months

### UI/UX
- **Responsive Design** - Mobile-first design that works on all devices
- **Dark/Light Theme** - Automatic theme switcher with preference saving
- **Modern UI** - Clean, professional interface with Bootstrap 5
- **Smooth Animations** - Enhanced user experience with CSS transitions

## 🛠 Tech Stack

### Backend
- **Python 3.x** - Programming language
- **Django 5.2.6** - Web framework
- **SQLite3** - Development database (can be upgraded to PostgreSQL)
- **Django Authentication** - User authentication system
- **Sessions** - Session management for visitor tracking

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with custom CSS
- **JavaScript (ES6)** - Client-side logic
- **Bootstrap 5.3.3** - UI framework
- **Font Awesome 6.4.0** - Icons
- **AJAX** - Async data loading

### Email & Communication
- **SMTP** - Email delivery (Gmail, Outlook, Yahoo, etc.)
- **OTP Email Verification** - 6-digit code verification
- **Email Notifications** - Visitor arrival notifications

### Additional Packages
- **python-dotenv** - Environment variable management
- **Pillow** - Image handling for visitor photos

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd visitor_management
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install django==5.2.6
pip install python-dotenv
pip install Pillow
```

### Step 4: Run Migrations
```bash
cd visitor_portal
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### Step 6: Import Employees
```bash
python manage.py import_employees visitors/data/employees.csv
```

### Step 7: Add Your Logo
Place your logo file at `visitor_portal/static/img/logo.png`

## 🚀 Quick Start

### Running the Development Server
```bash
cd visitor_portal
python manage.py runserver
```

Access the application:
- **Visitor Form**: http://127.0.0.1:8000/
- **Guard Dashboard**: http://127.0.0.1:8000/control/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root (`visitor_management/.env`):

```env
# Email Configuration
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your.email@gmail.com

# Optional: Twilio (if you want to add SMS later)
# TWILIO_ACCOUNT_SID=
# TWILIO_AUTH_TOKEN=
# TWILIO_FROM_NUMBER=
```

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed email configuration.

## 📁 Project Structure

```
visitor_portal/
├── manage.py                          # Django management script
├── db.sqlite3                         # SQLite database (dev)
├── README.md                          # This file
├── EMAIL_SETUP.md                     # Email configuration guide
│
├── visitor_portal/                    # Main project directory
│   ├── settings.py                     # Django settings
│   ├── urls.py                         # URL routing
│   ├── wsgi.py                         # WSGI configuration
│   └── asgi.py                         # ASGI configuration
│
├── visitors/                           # Main app
│   ├── models.py                       # Database models
│   ├── views.py                        # View logic
│   ├── urls.py                         # App URLs
│   ├── admin.py                        # Admin configuration
│   ├── email.py                        # Email functions
│   │
│   ├── templates/
│   │   └── visitors/
│   │       ├── intake.html             # Visitor form
│   │       ├── visit_detail.html       # Visit details
│   │       ├── dashboard.html          # Guard dashboard
│   │       └── login.html              # Login page
│   │
│   ├── data/
│   │   └── employees.csv               # Employee data
│   │
│   └── management/
│       └── commands/
│           ├── import_employees.py     # Import command
│           ├── export_employees.py    # Export command
│           └── load_sample_employees.py
│
├── static/                             # Static files
│   ├── css/
│   │   └── app.css                     # Custom styles
│   └── img/
│       └── logo.png                    # Company logo
│
└── media/                              # Uploaded files
    ├── visitor_photos/                 # Visitor photos
    └── visitor_ids/                    # ID documents
```

## 🎯 Usage

### Visitor Check-in Flow

1. **Visitor enters details**:
   - Full name
   - Email address
   - Address
   - Phone number

2. **Email OTP Verification**:
   - Visitor clicks "Send OTP" button
   - System sends 6-digit code to email
   - Visitor enters OTP to verify

3. **Select Employee**:
   - Type or select from dropdown
   - Search by name or department

4. **Purpose of Visit**:
   - Enter meeting purpose

5. **Complete Check-in**:
   - Visit is created with "ongoing" status
   - Email notification sent to employee
   - Visitor sees their visit details page

### Ending a Visit

Visitors can end their visit anytime from the visit detail page. The duration is automatically calculated and saved.

## 👥 Managing Employees

### Adding New Employees

#### Method 1: Edit CSV and Import (Recommended)

1. **Edit the CSV file**:
   ```bash
   # Navigate to the file
   visitors/data/employees.csv
   ```

2. **Add new employee row**:
   ```csv
   name,department,phone,email,active
   John Doe,IT,9876543210,john.doe@company.com,1
   ```

3. **Run import command**:
   ```bash
   python manage.py import_employees visitors/data/employees.csv
   ```

#### Method 2: Django Admin

1. Access admin: http://127.0.0.1:8000/admin/
2. Navigate to "Visitors" → "Employees"
3. Click "Add Employee"
4. Fill in details and save

### CSV Format

The CSV file must have these columns:
- **name** (required) - Employee full name
- **department** (required) - Department name
- **phone** (required) - Phone number (10 digits)
- **email** (optional) - Email address
- **active** (optional) - Active status (1 = active, 0 = inactive)

Example:
```csv
name,department,phone,email,active
Karan Kohli,Director,9999904285,karan.kohli@company.com,1
Om Prakash Jha,HR,8745041868,omprakash.jha@company.com,1
```

### Importing Employees

Run from the `visitor_portal` directory:
```bash
# Windows PowerShell
cd C:\path\to\visitor_management\visitor_portal
python manage.py import_employees visitors/data/employees.csv

# Linux/Mac
cd /path/to/visitor_management/visitor_portal
python manage.py import_employees visitors/data/employees.csv
```

**What the import does:**
- Creates new employees if they don't exist
- Updates existing employees with new information
- Preserves employee IDs (important for maintaining visit history)
- Can deactivate missing employees (with `--deactivate-missing` flag)

### Exporting Employees

```bash
python manage.py export_employees output.csv
```

## 📧 Email Setup

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for complete email configuration guide.

### Quick Setup for Gmail

1. Enable 2-Step Verification in your Google Account
2. Generate an App Password
3. Add to `.env` file:
   ```env
   EMAIL_HOST_USER=your.email@gmail.com
   EMAIL_HOST_PASSWORD=your_16_char_app_password
   ```
4. Test the email:
   - Run the server
   - Try to check in as a visitor
   - Check email for OTP

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### Making Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser
```bash
python manage.py createsuperuser
```

### View Database
```bash
python manage.py dbshell
```

## 🚀 Production Deployment

### Recommended Changes

1. **Use PostgreSQL**:
   ```bash
   pip install psycopg2-binary
   ```
   Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'visitor_db',
           'USER': 'db_user',
           'PASSWORD': 'db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **Set Secret Key**:
   ```python
   SECRET_KEY = os.getenv('SECRET_KEY')
   ```

3. **Disable Debug Mode**:
   ```python
   DEBUG = False
   ```

4. **Set Allowed Hosts**:
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

5. **Use Production WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn visitor_portal.wsgi:application
   ```

6. **Static Files**:
   ```bash
   python manage.py collectstatic
   ```

7. **Media Files**:
   - Use cloud storage (AWS S3, Google Cloud Storage)
   - Or configure nginx to serve media files

### Security Checklist
- [ ] Change `SECRET_KEY`
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS
- [ ] Set up firewall rules
- [ ] Use strong database passwords
- [ ] Enable Django security features
- [ ] Regular backups

## 📊 Database Models

### Employee
- `name` - Full name
- `department` - Department
- `phone` - Phone number
- `email` - Email address
- `active` - Active status

### Visitor
- `full_name` - Visitor name
- `email` - Email address
- `phone` - Phone number
- `address` - Address
- `photo` - Visitor photo
- `govt_id_type` - ID type (Aadhaar, PAN, etc.)
- `govt_id_image` - ID image
- `created_at` - Creation timestamp

### Visit
- `visitor` - Foreign key to Visitor
- `employee` - Foreign key to Employee
- `purpose` - Purpose of visit
- `started_at` - Visit start time
- `ended_at` - Visit end time
- `status` - Visit status (ongoing/ended)
- `sms_sent_at` - Notification time
- `notes` - Additional notes

## 🔗 Important URLs

- **Visitor Check-in**: `/`
- **Visit Details**: `/visit/<id>/`
- **End Visit**: `/visit/<id>/end/`
- **Guard Dashboard**: `/control/`
- **Guard Visit Details**: `/control/visit/<id>/`
- **Login**: `/login/`
- **Logout**: `/logout/`
- **Admin Panel**: `/admin/`
- **Password Reset**: `/password-reset/`
- **Password Change**: `/password-change/`

## 📝 Notes

- Uploaded photos and IDs are stored under `visitor_portal/media/`
- For production, use PostgreSQL and cloud storage for media
- Email functionality requires SMTP server access
- OTP codes expire after 5 minutes
- Visit sessions are tracked using Django sessions

## 🐛 Troubleshooting

### Email Not Sending
- Check `.env` file exists and has correct credentials
- Verify app password (not regular password for Gmail)
- Check spam folder
- Ensure SMTP port 587 is open

### OTP Not Working
- Check email address is valid
- Verify OTP hasn't expired (5 minutes)
- Check email credentials in settings

### Employee Not Appearing
- Ensure employee is marked as active (1)
- Run import command again
- Check CSV format is correct

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

## 📄 License

This project is proprietary software.

## 👨‍💻 Created By

Visitor Management System for Eterna Global Solutions LLP

---

**Last Updated**: 2025
**Version**: 1.0.0
