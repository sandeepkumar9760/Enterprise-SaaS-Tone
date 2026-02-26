# Enterprise-SaaS-Tone 🎓

## An AI-Driven Academic Workflow Platform for Intelligent Make-Up Scheduling, Secure Code-Based Attendance, and Predictive Classroom Optimization

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0.2-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Database Configuration](#database-configuration)
- [How to Run](#how-to-run)
- [API Endpoints](#api-endpoints)
- [Usage Guide](#usage-guide)
- [Models Architecture](#models-architecture)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**Enterprise-SaaS-Tone** is a modern, enterprise-grade academic management system designed to streamline make-up class scheduling and attendance tracking for educational institutions. Built with Django and PostgreSQL, this platform offers:

- 🔐 **Secure Authentication System** for Admin, Faculty, and Students
- 📊 **Real-time Dashboard Analytics** with attendance metrics
- 🎯 **Intelligent Remedial Code System** for quick attendance marking
- 🤖 **AI-Powered Insights** for predictive classroom optimization
- 📱 **Responsive UI** with modern design principles

---

## ✨ Key Features

### For Administrators & Faculty
- ✅ Create and manage make-up classes with auto-generated remedial codes
- ✅ Track student attendance in real-time
- ✅ View comprehensive dashboard with statistics
- ✅ Edit or delete scheduled classes
- ✅ Access AI-driven analytics for trend analysis

### For Students
- ✅ Mark attendance using unique remedial codes
- ✅ View personal attendance history
- ✅ Track attendance metrics and pending sessions
- ✅ Simple, intuitive interface

### Technical Highlights
- ✅ RESTful API architecture
- ✅ PostgreSQL database with optimized queries
- ✅ Auto-generated unique codes (RC-XXXXXX format)
- ✅ Timezone-aware date/time handling
- ✅ Duplicate attendance prevention
- ✅ Role-based access control (RBAC)

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 6.0.2
- **Language**: Python 3.11+
- **Database**: PostgreSQL
- **ORM**: Django ORM
- **Authentication**: Django Auth System

### Frontend
- **Templates**: Django Template Engine
- **Styling**: Custom CSS with responsive design
- **JavaScript**: Vanilla JS for dynamic interactions

### Dependencies
```
asgiref==3.11.1
Django==6.0.2
psycopg2-binary==2.9.11
sqlparse==0.5.5
tzdata==2025.3
```

---

## 📁 Project Structure

```
Enterprise-SaaS-Tone/
│
├── makeup_backend/           # Main Django app
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   ├── admin_login.html  # Admin login page
│   │   ├── index.html        # Dashboard
│   │   ├── faculty.html      # Faculty management
│   │   ├── student.html      # Student portal
│   │   └── ai_insights.html  # AI analytics
│   ├── __init__.py
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   ├── models.py             # Database models
│   ├── signals.py            # Django signals
│   ├── tests.py              # Unit tests
│   ├── urls.py               # URL routing
│   └── views.py              # View logic & APIs
│
├── makeup_class/             # Django project settings
│   ├── __init__.py
│   ├── asgi.py               # ASGI configuration
│   ├── settings.py           # Project settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI configuration
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── makeup_dbs                # Database name reference
└── README.md                 # This file
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python**: Version 3.11 or higher
- **PostgreSQL**: Version 12 or higher
- **pip**: Python package manager
- **Virtual Environment**: `venv` or `virtualenv` (recommended)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/sandeepkumar9760/Enterprise-SaaS-Tone.git
cd Enterprise-SaaS-Tone
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Configuration

### Step 1: Install PostgreSQL

Download and install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

### Step 2: Create Database

```sql
-- Open PostgreSQL command line or pgAdmin
CREATE DATABASE makeup_dbs;
```

### Step 3: Configure Database Settings

The project is pre-configured with the following settings in `makeup_class/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'makeup_dbs',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**⚠️ Important**: Update these credentials based on your PostgreSQL installation:
- `USER`: Your PostgreSQL username (default: `postgres`)
- `PASSWORD`: Your PostgreSQL password
- `HOST`: Database host (default: `localhost`)
- `PORT`: PostgreSQL port (default: `5432`)

---

## ▶️ How to Run

### Step 1: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates all necessary database tables:
- `auth_user` - User authentication
- `makeup_backend_userprofile` - User roles (Admin, Faculty, Student)
- `makeup_backend_faculty` - Faculty information
- `makeup_backend_student` - Student records
- `makeup_backend_makeupclass` - Make-up class schedules
- `makeup_backend_attendance` - Attendance records

### Step 2: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Enter your desired admin credentials:
- Username
- Email
- Password

### Step 3: Start Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

### Step 4: Access Admin Panel

Navigate to: **http://127.0.0.1:8000/admin-login/**

Login with the superuser credentials you created.

---

## 🔗 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/admin-login/` | Admin login |
| GET | `/admin-logout/` | Admin logout |

### Page Views

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard homepage |
| GET | `/faculty/` | Faculty management page |
| GET | `/student/` | Student portal page |
| GET | `/ai/` | AI insights page |

### Dashboard APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/` | Get dashboard statistics |

### Faculty APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/faculty/create-class/` | Create new make-up class |
| GET | `/api/faculty/classes/` | List all make-up classes |
| POST | `/api/faculty/delete-class/<int:class_id>/` | Delete a class |
| POST | `/api/faculty/edit-class/<int:class_id>/` | Edit class details |

### Student APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/student/mark-attendance/` | Mark attendance using code |
| GET | `/api/student/history/` | Get attendance history |
| GET | `/api/student/metrics/` | Get attendance metrics |

### AI Analytics APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ai/analytics/` | Get AI-driven trend analysis |

---

## 📖 Usage Guide

### Creating a Make-Up Class (Faculty)

1. Navigate to **Faculty** section
2. Click **Create New Class**
3. Fill in the form:
   - Subject name
   - Classroom number
   - Date (YYYY-MM-DD format)
   - Time (HH:MM format)
4. Submit - A unique **Remedial Code** will be auto-generated

### Marking Attendance (Student)

1. Navigate to **Student** section
2. Enter the **Remedial Code** provided by faculty
3. Click **Mark Attendance**
4. Confirmation message will appear

### Viewing Analytics (Admin)

1. Navigate to **Dashboard**
2. View real-time statistics:
   - Total classes scheduled
   - Total students enrolled
   - Total attendance marked
   - Attendance rate percentage
3. Navigate to **AI Insights** for trend analysis

---

## 🏗️ Models Architecture

### UserProfile
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # ROLE_CHOICES: ADMIN, FACULTY, STUDENT
```

### Faculty
```python
class Faculty(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
```

### Student
```python
class Student(models.Model):
    name = models.CharField(max_length=150)
    roll_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
```

### MakeUpClass
```python
class MakeUpClass(models.Model):
    subject = models.CharField(max_length=100)
    classroom = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    remedial_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Auto-generates format: RC-XXXXXX (e.g., RC-A3F2E1)
```

### Attendance
```python
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    makeup_class = models.ForeignKey(MakeUpClass, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'makeup_class')  # Prevents duplicates
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Sandeep Kumar**
- GitHub: [@sandeepkumar9760](https://github.com/sandeepkumar9760)
- Repository: [Enterprise-SaaS-Tone](https://github.com/sandeepkumar9760/Enterprise-SaaS-Tone)

---

## 🙏 Acknowledgments

- Django Framework for robust backend development
- PostgreSQL for reliable database management
- Open-source community for continuous support

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/sandeepkumar9760/Enterprise-SaaS-Tone/issues)
- Contact via GitHub profile

---

**Made with ❤️ for Educational Excellence**
