# 🎓 EdTech Student Registration System

<div align="center">

![Django](https://img.shields.io/badge/Django-5.1-green.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A secure, professional student registration system with encryption, duplicate prevention, and email confirmation**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Testing](#-testing) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
  - [Core Requirements](#-core-requirements)
  - [Additional Features](#-additional-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Security Features](#-security-features)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This is a comprehensive **Student Registration System** built for EdTech companies. The system provides a secure, user-friendly platform for students to register with encrypted data storage, automatic email confirmations, and robust duplicate prevention mechanisms.

### Key Highlights

- 🔐 **End-to-end encryption** for sensitive data (email & mobile)
- 🎨 **Modern, professional UI** with smooth animations
- ✅ **Hash-based duplicate prevention** system
- 📧 **Automated email confirmations** with registration IDs
- 🧪 **Comprehensive test suite** with 18+ test cases
- 📊 **Django Admin integration** for data management
- 🚀 **Production-ready** codebase with best practices

---

## ✨ Features

### Core Requirements ✅

#### 1. ✅ Student Database Table
- **Table Structure**: `student` table with all required fields
  - `id` - Primary Key (Auto-increment)
  - `name` - Student full name (VARCHAR)
  - `email` - Encrypted email (VARBINARY for encrypted storage)
  - `mobile` - Encrypted mobile (VARBINARY for encrypted storage)
  - `student_class` - Class/Grade information (VARCHAR)
  - `created` - Timestamp (auto-set on creation)
  - `modified` - Timestamp (auto-updates on change)

- **Database**: MySQL with manual table creation (no Django migrations)
- **SQL Script**: Located in `sql_scripts/student_table.sql`

#### 2. ✅ Student Registration Page
- **Beautiful, Modern UI** with:
  - Gradient backgrounds and smooth animations
  - Bootstrap 5 integration
  - Bootstrap Icons for visual enhancement
  - Responsive design (mobile-friendly)
  - Form validation with real-time error messages
  - Loading states and user feedback

- **Form Features**:
  - Name field (required)
  - Email field with format validation (required)
  - Mobile field with digit validation (required, min 10 digits)
  - Class field (optional)
  - Client-side and server-side validation

#### 3. ✅ Data Encryption
- **Encryption Method**: Fernet symmetric encryption (cryptography library)
- **Encrypted Fields**: Email and Mobile numbers
- **Storage Format**: VARBINARY in MySQL database
- **Security**: 
  - Encryption key stored in Django settings
  - One-way hash comparison for duplicate detection
  - Data remains encrypted at rest

#### 4. ✅ Email Confirmation System
- **Automatic Email Sending** after successful registration
- **Email Content**:
  - Professional HTML email template
  - Registration ID prominently displayed
  - Student name and details
  - Confirmation message
- **Email Configuration**:
  - SMTP support (Gmail, Outlook, custom)
  - Console backend for development
  - Configurable email settings

---

### Additional Features 🚀

#### 1. 🔒 Hash-Based Duplicate Prevention System
**Beyond basic requirements** - A sophisticated duplicate detection system:

- **Hash-Based Comparison**: Uses SHA256 hashing for duplicate detection
- **Case-Insensitive**: Email comparison works regardless of case
- **Format-Independent**: Mobile numbers compared by digits only
- **Real-Time Validation**: Prevents duplicates during form submission
- **Clear Error Messages**: User-friendly duplicate detection messages

**How it works**:
```
User Input → Normalize → Hash → Compare with existing hashes → Reject if duplicate
```

**Benefits**:
- Works with encrypted data without decrypting all records
- Handles edge cases (case differences, formatting variations)
- Prevents duplicate registrations effectively
- Maintains data integrity

#### 2. 🎨 Professional UI/UX Design
**Enhanced user experience** with modern design:

- **Visual Design**:
  - Gradient color schemes
  - Smooth animations and transitions
  - Professional typography
  - Icon integration (Bootstrap Icons)
  - Card-based layouts

- **User Experience**:
  - Loading states on form submission
  - Auto-dismissing alerts
  - Success animations (confetti effect)
  - Responsive design for all devices
  - Clear visual hierarchy

#### 3. 📊 Django Admin Integration
**Management interface** for administrators:

- **Features**:
  - View all registered students
  - **Decrypted data display** (email & mobile visible)
  - Search and filter capabilities
  - Encrypted data preview (hex format)
  - Read-only registration (prevents admin creation)
  - Secure access control

#### 4. 🧪 Comprehensive Test Suite
**18+ test cases** covering complete application flow:

- **Test Categories**:
  - Encryption/Decryption tests
  - Form validation tests
  - Registration flow tests
  - Database operation tests
  - **Integration test** (complete end-to-end flow)

- **Documentation**: Each test includes detailed comments explaining the flow
- **Coverage**: Tests all major functions and edge cases

#### 5. 📝 Management Commands
**Command-line tools** for data viewing:

- `python manage.py view_students` - View all students with decrypted data
- `python manage.py view_students --id 3` - View specific student
- Displays decrypted email and mobile numbers
- Formatted output with all student details

#### 6. 🔧 Enhanced Error Handling
**Robust error management**:

- Form validation errors with clear messages
- Database error handling
- Email sending error handling (non-blocking)
- User-friendly error messages
- Console logging for debugging

#### 7. 📚 Comprehensive Documentation
**Multiple documentation files**:

- `SETUP_INSTRUCTIONS.md` - Database and environment setup
- `EMAIL_SETUP.md` - Email configuration guide
- `VIEW_DATA.md` - Data viewing methods
- `DUPLICATE_PREVENTION.md` - Duplicate prevention system details
- Inline code comments and docstrings

#### 8. 🛡️ Security Enhancements
**Additional security measures**:

- CSRF protection enabled
- Secure session management
- Environment-based configuration
- Encryption key management
- Input sanitization and validation

#### 9. 🎯 URL Routing & Navigation
**Clean URL structure**:

- Root URL redirects to registration
- RESTful URL patterns
- Namespaced URLs for better organization
- Success page routing

#### 10. 📧 Email Template System
**Professional email templates**:

- HTML email templates
- Responsive email design
- Branded email content
- Registration ID display
- Template rendering system

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 5.1 |
| **Database** | MySQL 8.0 |
| **Python Version** | 3.11+ |
| **Encryption** | Fernet (cryptography library) |
| **Frontend** | Bootstrap 5, Bootstrap Icons |
| **Email** | Django Email Backend (SMTP) |
| **Database Adapter** | PyMySQL |

---

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sikorsky3301/AhaGuru-Student-Registration.git
cd AhaGuru-Student-Registration
```

### Step 2: Install Dependencies

```bash
pip install django PyMySQL cryptography
```

### Step 3: Database Setup

1. **Create MySQL Database**:
   ```sql
   CREATE DATABASE edtech_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Create Student Table**:
   - Open MySQL Workbench or command line
   - Run the SQL script: `sql_scripts/student_table.sql`
   - Or execute:
     ```sql
     USE edtech_db;
     CREATE TABLE student (
         id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(255) NOT NULL,
         email VARBINARY(255) NOT NULL,
         mobile VARBINARY(255) NOT NULL,
         student_class VARCHAR(100),
         created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
     );
     ```

### Step 4: Configure Django Settings

1. **Update Database Credentials** in `core/core/settings.py`:
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.mysql",
           "NAME": "edtech_db",
           "USER": "your_username",
           "PASSWORD": "your_password",
           "HOST": "localhost",
           "PORT": "3306",
       }
   }
   ```

2. **Configure Email Settings** (optional, for production):
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'
   DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
   ```

### Step 5: Run Migrations

```bash
cd core
python manage.py migrate
```

This creates Django system tables (sessions, admin, etc.)

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Run the Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## ⚙️ Configuration

### Email Setup

For Gmail:
1. Enable 2-Step Verification
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Update `EMAIL_HOST_PASSWORD` in settings.py

See `EMAIL_SETUP.md` for detailed instructions.

### Encryption Key

The encryption key is automatically generated on first use. For production, set it in `settings.py`:

```python
ENCRYPTION_KEY = 'your-encryption-key-here'
```

---

## 🚀 Usage

### Student Registration

1. Navigate to: `http://127.0.0.1:8000/register/`
2. Fill out the registration form:
   - Name (required)
   - Email (required, will be encrypted)
   - Mobile (required, will be encrypted)
   - Class (optional)
3. Submit the form
4. Receive confirmation email with Registration ID
5. View success page with registration details

### Viewing Data

**Method 1: Django Admin**
- Go to: `http://127.0.0.1:8000/admin/`
- Login with superuser credentials
- Click "Students" → "Students"
- View all students with decrypted data

**Method 2: Command Line**
```bash
python manage.py view_students
```

**Method 3: MySQL Workbench**
```sql
SELECT id, name, student_class, created FROM student;
```

See `VIEW_DATA.md` for more methods.

---

## 📁 Project Structure

```
edtech-student-registration/
│
├── core/                          # Django project root
│   ├── core/                      # Main project settings
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # URL routing
│   │   └── __init__.py           # PyMySQL configuration
│   │
│   ├── students/                 # Students app
│   │   ├── models.py             # Student model
│   │   ├── views.py              # Registration views
│   │   ├── forms.py              # Registration form
│   │   ├── encryption.py         # Encryption utilities
│   │   ├── admin.py              # Django admin config
│   │   ├── urls.py               # App URLs
│   │   ├── tests.py              # Test suite
│   │   │
│   │   ├── templates/            # HTML templates
│   │   │   └── students/
│   │   │       ├── register.html
│   │   │       ├── success.html
│   │   │       └── emails/
│   │   │           └── registration_confirmation.html
│   │   │
│   │   └── management/           # Management commands
│   │       └── commands/
│   │           └── view_students.py
│   │
│   └── manage.py                 # Django management script
│
├── sql_scripts/                   # SQL scripts
│   └── student_table.sql         # Table creation script
│
├── database/                      # Database files
│   └── student_table.sql
│
└── Documentation/                 # Documentation files
    ├── SETUP_INSTRUCTIONS.md
    ├── EMAIL_SETUP.md
    ├── VIEW_DATA.md
    └── DUPLICATE_PREVENTION.md
```

---

## 🔐 Security Features

### Data Encryption
- **Algorithm**: Fernet (symmetric encryption)
- **Encrypted Fields**: Email and Mobile
- **Storage**: VARBINARY in MySQL
- **Key Management**: Stored in Django settings (use environment variables in production)

### Duplicate Prevention
- **Method**: SHA256 hash-based comparison
- **Features**:
  - Case-insensitive email matching
  - Format-independent mobile matching
  - Real-time validation
  - Prevents duplicate registrations

### Security Best Practices
- CSRF protection enabled
- Input validation and sanitization
- Secure session management
- SQL injection prevention (parameterized queries)
- XSS protection (Django template escaping)

---

## 🧪 Testing

### Run All Tests

```bash
cd core
python manage.py test students
```

### Run Specific Test Cases

```bash
# Encryption tests
python manage.py test students.tests.EncryptionTestCase

# Form validation tests
python manage.py test students.tests.FormValidationTestCase

# Integration test (complete flow)
python manage.py test students.tests.IntegrationTestCase
```

### Test Coverage

- ✅ Encryption/Decryption (3 tests)
- ✅ Form Validation (8 tests)
- ✅ Registration Flow (4 tests)
- ✅ Database Operations (2 tests)
- ✅ Integration Test (1 comprehensive test)

**Total: 18+ test cases** covering all major functionality

---

## 📚 Documentation

### Available Documentation

1. **SETUP_INSTRUCTIONS.md** - Complete setup guide
2. **EMAIL_SETUP.md** - Email configuration instructions
3. **VIEW_DATA.md** - Methods to view student data
4. **DUPLICATE_PREVENTION.md** - Duplicate prevention system details

### Code Documentation

- Comprehensive docstrings in all functions
- Inline comments explaining complex logic
- Test cases serve as usage examples
- README with complete feature list

---

## 📸 Screenshots

### Registration Page
- Modern gradient design
- Form with icons and validation
- Responsive layout

### Success Page
- Animated success icon
- Registration ID display
- Email confirmation message
- Professional styling

### Admin Panel
- Decrypted data view
- Search and filter options
- Encrypted data preview

---

## 🚀 Future Enhancements

### Planned Features

- [ ] **Bulk Registration**: CSV import functionality
- [ ] **Student Dashboard**: Personal student portal
- [ ] **Email Templates**: Multiple template options
- [ ] **Analytics Dashboard**: Registration statistics
- [ ] **API Endpoints**: REST API for mobile apps
- [ ] **Two-Factor Authentication**: Enhanced security
- [ ] **Export Functionality**: Export data to Excel/PDF
- [ ] **Email Verification**: Click-to-verify email links
- [ ] **Password Reset**: For registered students
- [ ] **Multi-language Support**: Internationalization

### Performance Improvements

- [ ] Database indexing for faster queries
- [ ] Caching for duplicate checks
- [ ] Async email sending
- [ ] Pagination for large datasets

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Rishi Raj**

- GitHub: [@Sikorsky3301](https://github.com/Sikorsky3301)
- Project: [AhaGuru Student Registration](https://github.com/Sikorsky3301/AhaGuru-Student-Registration)

---

## 🙏 Acknowledgments

- Django Framework
- Bootstrap for UI components
- Cryptography library for encryption
- MySQL for database
- All contributors and testers

---

<div align="center">

**⭐ If you find this project useful, please give it a star! ⭐**

Made with ❤️ for EdTech

</div>
