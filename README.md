*Uni-Connect — Student Academic Discussion Forum*

<div align="center">

![Uni-Connect Banner](https://img.shields.io/badge/Uni--Connect-Student%20Academic%20Forum-7C3AED?style=for-the-badge&logo=discourse&logoColor=white)

[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-F59E0B?style=flat-square)]()

**A web-based academic discussion platform built for university students and lecturers.**  
Replacing fragmented WhatsApp groups with structured, searchable, course-organised knowledge — built at the Department of Computer Science, University of Nigeria, Nsukka.

[Features](#features) · [Demo](#demo) · [Installation](#installation) · [Usage](#usage) · [Architecture](#architecture) · [Contributing](#contributing)

</div>

---

## Overview

<img width="1365" height="651" alt="image" src="https://github.com/user-attachments/assets/4f30e576-4dbe-4ea8-807c-fb41c1559fea" />


Uni-Connect is a full-stack web application that provides Nigerian university students and lecturers with a dedicated space for academic discourse. Unlike informal tools such as WhatsApp or Telegram, Uni-Connect organises discussions by department and course, preserves knowledge across academic sessions, and introduces a content verification system through peer upvoting and lecturer-endorsed answers.

<img width="1365" height="651" alt="image" src="https://github.com/user-attachments/assets/f677caca-cbfd-4fa9-adba-107ee217fe56" />


The platform was developed as a final-year capstone project at the **Department of Computer Science, University of Nigeria, Nsukka**, in partial fulfilment of the requirements for the award of a Bachelor of Science (B.Sc.) degree in Computer Science.

> **Supervisor:** Prof. C.N. Udanor, Department of Computer Science, UNN

---

## Features

### For Students
- 📝 **Post Questions** — create threaded discussions scoped to a specific course
<img width="1365" height="651" alt="image" src="https://github.com/user-attachments/assets/56dc29a8-f5dd-41b8-9116-6b25d7829b18" />

- 💬 **Nested Replies** — respond to threads or to individual comments
- ⬆️ **Peer Voting** — upvote and downvote answers to surface the most helpful responses
- 🔍 **Full-Text Search** — search across all threads, replies, and tags from every academic session
<img width="1365" height="651" alt="image" src="https://github.com/user-attachments/assets/41206f5a-1415-4aa3-8f01-d8a32918e1ae" />

- 🏆 **Reputation System** — earn points for upvotes received and endorsed answers
<img width="1365" height="651" alt="image" src="https://github.com/user-attachments/assets/b0bee248-31af-4479-9009-bf67bbc95a44" />

<img width="1365" height="651" alt="image" src="https://github.com/user-attachments/assets/d05b3f5a-5db6-4975-adba-ced857b4e9d5" />


- 🔔 **Notifications** — get alerted on replies, mentions, and endorsements

### For Lecturers
- ⭐ **Endorse Answers** — mark a reply as a Verified Answer within your own courses
- 📌 **Pin Threads** — pin important announcements or exam revision threads
- 🔒 **Lock Threads** — close resolved or outdated discussions
- 🛡️ **Course Moderation** — flag or remove inappropriate content within assigned courses

### For Administrators
- 🏛️ **Department Management** — register departments and assign departmental admins
<img width="1365" height="651" alt="image" src="https://github.com/user-attachments/assets/70bbefdd-e79c-4d54-a605-62859a26f34e" />

- 📚 **Course Management** — create, edit, and deactivate courses across departments
- 👥 **User Management** — approve lecturer accounts and manage role assignments
- 📊 **Platform Analytics** — view engagement metrics, thread activity, and usage stats
- 🚩 **Content Moderation** — review flagged content, restore soft-deleted posts, audit logs

### Platform-Wide
- 📱 **Mobile-First Design** — fully responsive, optimised for low-bandwidth mobile data connections
- 🎨 **3D Hero Interface** — Spline-powered 3D animation on the landing page and authentication screens
<img width="1365" height="651" alt="image" src="https://github.com/user-attachments/assets/38d2996c-b67e-4584-909f-55e3e4ec712a" />

- 🌙 **Dark Theme** — deep navy/violet/cyan/amber palette designed for extended reading sessions
- 🔐 **Role-Based Access Control** — student, lecturer, and admin permissions enforced at every route
- 🛡️ **Security** — CSRF protection, session management, input sanitisation, parameterised queries

---

## Demo

> **Live Demo:** *(Add your deployed URL here — e.g. Render, Railway, or PythonAnywhere)*

### Quick Demo Logins

| Role | Email | Password |
|------|-------|----------|
| Student | `student@unn.edu.ng` | `demo1234` |
| Lecturer | `lecturer@unn.edu.ng` | `demo1234` |
| Admin | `admin@unn.edu.ng` | `demo1234` |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11, Django 4.2 LTS |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Vanilla JavaScript |
| **Database** | SQLite (development) → PostgreSQL (production) |
| **Typography** | Space Grotesk, Fraunces (Google Fonts) |
| **Auth** | Django built-in authentication + RBAC |
| **Security** | CSRF tokens, PBKDF2-SHA256 hashing, parameterised ORM queries |

---

## Architecture

The system follows Django's **Model-View-Template (MVT)** pattern across a three-tier architecture:

```
┌─────────────────────────────────────────────────────┐
│  Presentation Tier                                  │
│  HTML5 + CSS3 + Bootstrap 5 + Vanilla JS + Spline  │
└────────────────────┬────────────────────────────────┘
                     │ HTTP
┌────────────────────▼────────────────────────────────┐
│  Business Logic Tier                                │
│  Django Views · RBAC · Voting · Endorsement Logic  │
└────────────────────┬────────────────────────────────┘
                     │ Django ORM
┌────────────────────▼────────────────────────────────┐
│  Data Tier                                          │
│  SQLite (dev) / PostgreSQL (prod)                  │
└─────────────────────────────────────────────────────┘
```

### Project Structure

```
uniconnect/
├── uniconnect/
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                # Authentication & user management
│   ├── models.py            # User, Department
│   ├── views.py             # Register, login, profile
│   ├── forms.py
│   └── urls.py
│
├── forum/                   # Core discussion logic
│   ├── models.py            # Course, Thread, Reply, Vote, Endorsement, Notification, Reputation
│   ├── views.py             # Thread CRUD, voting, endorsement, search, moderation
│   ├── forms.py
│   └── urls.py
│
├── static/
│   └── uniconnect/
│       ├── css/
│       │   ├── style.css    # Main design system
│       │   └── auth.css     # Auth page styles
│       └── js/
│           ├── main.js      # Landing page & Spline embed
│           └── auth.js      # Auth interactions & fallback
│
├── templates/
│   ├── base.html
│   ├── index.html           # Landing page
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   ├── thread_list.html
│   └── thread_detail.html
│
├── db.sqlite3               # Development database
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.11 or later
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/uni-connect.git
cd uni-connect
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

> Generate a secret key with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. (Optional) Load Sample Data

```bash
python manage.py loaddata fixtures/sample_data.json
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Production Deployment

### Migrating to PostgreSQL

1. Install PostgreSQL and the adapter:

```bash
pip install psycopg2-binary
```

2. Update your `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/uniconnect
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

3. Run migrations against the new database:

```bash
python manage.py migrate
```

### Static Files

```bash
python manage.py collectstatic
```

### Recommended Hosting

| Platform | Notes |
|----------|-------|
| [Railway](https://railway.app) | Simple, free tier, PostgreSQL included |
| [Render](https://render.com) | Free tier, easy Django deploy |
| [PythonAnywhere](https://pythonanywhere.com) | Beginner-friendly, Nigerian-accessible |

---

## Usage

### Posting a Question
1. Log in and navigate to your course
2. Click **Ask Question**
3. Add a title, body, and relevant tags
4. Submit — your thread is immediately visible to all course members

### Endorsing an Answer *(Lecturers only)*
1. Open a thread in your assigned course
2. Find the most accurate reply
3. Click **Endorse as Verified** — it receives a ⭐ badge and is ranked above all others

### Searching the Archive
- Use the search bar at the top of any page
- Filter by course, department, tag, or date
- Results include threads from all past academic sessions

---

## Database Schema (Summary)

| Table | Key Fields |
|-------|-----------|
| `auth_user` | id, username, email, password_hash, role, department_id, level |
| `departments` | id, name, created_date |
| `courses` | id, department_id, course_code, title, level |
| `threads` | id, course_id, author_id, title, body, status, created_date |
| `replies` | id, thread_id, parent_reply_id, author_id, body, vote_score, is_endorsed |
| `votes` | id, reply_id, user_id, direction |
| `notifications` | id, user_id, type, reference_id, is_read |
| `reputation` | id, user_id, points |

---

## Security

- **Authentication** — Django PBKDF2-SHA256 password hashing (260,000 iterations)
- **Sessions** — cryptographically signed cookies with inactivity expiry
- **CSRF** — token validation on all state-changing requests
- **Input** — server-side sanitisation and parameterised ORM queries
- **RBAC** — view-level permission enforcement by user role
- **OWASP** — mitigations aligned with the OWASP Top Ten

---

## Requirements

```
Django==4.2
Pillow==10.1.0
python-decouple==3.8
psycopg2-binary==2.9.9      # For PostgreSQL (production)
```

---

## Roadmap

- [x] User authentication and role management
- [x] Department and course organisation
- [x] Threaded discussions with nested replies
- [x] Peer upvoting and downvoting
- [x] Lecturer-endorsed verified answers
- [x] Full-text search across all sessions
- [x] Reputation system and leaderboard
- [x] In-app notifications
- [x] Admin moderation panel
- [x] Mobile-first responsive design
- [ ] Email notifications
- [ ] Password reset via email
- [ ] Dark/light theme toggle
- [ ] PDF/image attachment support
- [ ] Mobile application (iOS & Android)
- [ ] Multi-institution deployment support
- [ ] REST API for third-party integrations

---

## Contributing

Contributions are welcome, especially from students at UNN or other Nigerian institutions who want to adapt the platform for their own departments.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow the existing code style and include a brief description of what your contribution does and why.

---

## Academic Context

This project was submitted in partial fulfilment of the requirements for the award of:

**Bachelor of Science (B.Sc.) in Computer Science**  
Department of Computer Science  
University of Nigeria, Nsukka  
November 2025

**Author:** *(Igwesi Chiemerie Divine)*  
**Registration Number:** *(2021/243283)*  


---

## License

This project is released under the [MIT License](LICENSE). You are free to use, modify, and distribute it, provided attribution is maintained. See `LICENSE` for full terms.

---

## Acknowledgements

- Prof. C.N. Udanor — project supervision and guidance
- The Department of Computer Science, UNN — academic foundation
- All students and lecturers whose feedback shaped the platform's design
- The Django, Bootstrap, and Spline open-source communities

---

<div align="center">

Made with 💜 at the University of Nigeria, Nsukka

</div>
