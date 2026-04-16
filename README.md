# 🌍 ClimateWISE Youth Organization — Web Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Paystack](https://img.shields.io/badge/Payments-Paystack-00C3F7?style=flat)](https://paystack.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

The official web platform for **ClimateWISE Youth Organization (CYO)** — a youth-led organization championing climate resilience, WASH (Water, Sanitation and Hygiene), circular economy, and sustainable community development across Ghana and Africa.

This platform handles volunteer and partner registrations, contact inquiries, donations via Paystack (Mobile Money), and an internal admin dashboard for managing organizational data.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Getting Started (Local Development)](#-getting-started-local-development)
- [Environment Variables](#-environment-variables)
- [Database Migrations](#-database-migrations)
- [Paystack Integration](#-paystack-integration)
- [Admin Panel](#-admin-panel)
- [Docker Deployment (Nginx + Gunicorn)](#-docker-deployment-nginx--gunicorn)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌱 Project Overview

CYO's web platform serves two distinct audiences:

- **The Public** — Learns about CYO's mission, thematic areas, projects, and team; signs up as a volunteer or partner; and makes donations.
- **Administrators** — Views real-time impact data (volunteers, partners, donations, messages) through a secure internal dashboard.

**Key public-facing pages:**

| Page | URL |
|---|---|
| Home | `/` |
| About CYO | `/about/who-we-are` |
| Team | `/about/team` |
| Thematic Areas | `/thematic/...` |
| Projects & Impacts | `/projects-and-impacts` |
| Volunteer | `/get-in-touch/volunteers` |
| Partner | `/get-in-touch/partners` |
| Contact | `/get-in-touch/contact-us` |
| Donate | `/donation` |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Flask (Python) |
| Database ORM | SQLAlchemy + Flask-Migrate |
| Database | MySQL 8+ (production) / SQLite (development) |
| Forms & CSRF | Flask-WTF |
| Email | Flask-Mail |
| Payments | Paystack (Mobile Money — MTN, Vodafone, AirtelTigo) |
| Frontend | Bootstrap 5.3, Font Awesome 6.5, Jinja2 templates |
| Server | Gunicorn (WSGI) |
| Reverse Proxy | Nginx |
| Containerisation | Docker + Docker Compose |

---

## ✨ Features

### Public
- **Volunteer Registration** — Form submission stored in the database; duplicate email detection
- **Partner Registration** — Same as above with separate tracking
- **Contact Form** — Sends email notification asynchronously via Flask-Mail
- **Donations** — Full Paystack flow: initialize → checkout → callback → server-side verification → webhook fallback
- **Anonymous Donations** — Donors can hide their name from public display
- **Member Counter** — Live count of unique volunteers + partners (deduped by email) shown on the homepage

### Admin
- Secure login with role-based access (`developer`, `ceo`, `admin`)
- Dashboard with live volunteer, partner, donation, and message counts
- Chart.js analytics (donations over time, members breakdown)
- Recent activity feed
- Per-table data views

### Security
- CSRF protection on all forms (Flask-WTF)
- Rate limiting on payment and webhook endpoints
- Input sanitisation (email, phone, text, amounts)
- Paystack webhook HMAC-SHA512 signature verification
- Idempotent payment verification (prevents double-processing)
- Reference sanitisation to prevent injection attacks

---

## 📁 Project Structure

```
climatewise/
├── app/
│   ├── __init__.py          # Flask app factory, extensions init
│   ├── models.py            # SQLAlchemy models
│   ├── routes.py            # Public routes + Paystack payment flow
│   ├── admin_routes.py      # Admin dashboard routes
│   ├── utils.py             # Sanitisers, rate limiter, security headers
│   └── templates/
│       ├── public/          # Public-facing Jinja2 templates
│       │   ├── base.html
│       │   ├── home.html
│       │   ├── about.html
│       │   ├── volunteer.html
│       │   ├── partners.html
│       │   ├── donation.html
│       │   ├── paystack.html
│       │   ├── 404.html
│       │   └── 500.html
│       └── admin/           # Admin panel templates
│           ├── base_admin.html
│           └── dashboard.html
├── static/
│   ├── css/style.css
│   ├── js/
│   │   ├── index.js
│   │   └── dashboard.js
│   ├── images/
│   └── videos/
├── migrations/              # Flask-Migrate Alembic migration files
├── nginx/
│   └── nginx.conf           # Nginx reverse proxy config
├── .env                     # Environment variables (never commit this)
├── .env.example             # Template for environment variables
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── wsgi.py                  # Gunicorn entry point
└── README.md
```

---

## 🚀 Getting Started (Local Development)

### Prerequisites

- Python 3.11+
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Saviour99/climatewise.git
cd climatewise
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
# Then open .env and fill in your values (see Environment Variables section below)
```

### 5. Initialise the Database

```bash
flask db upgrade
```

### 6. Run the Development Server

```bash
flask run
```

The app will be available at `http://127.0.0.1:5000`.

---

## 🔐 Environment Variables

Create a `.env` file in the project root. **Never commit this file to version control.**

```dotenv
# ─── Flask Core ────────────────────────────────────────────────────────────────
FLASK_APP=wsgi.py
FLASK_ENV=development          # Use 'production' in deployment
SECRET_KEY=your-very-secret-key-here

# ─── Database ──────────────────────────────────────────────────────────────────
# Development (SQLite)
DATABASE_URL=sqlite:///climatewise.db

# Production (MySQL) — uncomment and fill in for deployment
# DATABASE_URL=mysql+pymysql://db_user:db_password@db_host:3306/climatewise_db

# ─── Email (Flask-Mail) ────────────────────────────────────────────────────────
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password      # Use a Gmail App Password, not your login password
USER_EMAIL=your-email@gmail.com      # Sender / recipient for contact form emails

# ─── Paystack ──────────────────────────────────────────────────────────────────
PAYSTACK_SECRET_KEY=sk_live_xxxxxxxxxxxxxxxxxxxx   # Use sk_test_... for testing
```

### Notes on sensitive values

| Variable | How to obtain |
|---|---|
| `SECRET_KEY` | Generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `MAIL_PASSWORD` | [Create a Gmail App Password](https://support.google.com/accounts/answer/185833) — do NOT use your regular Gmail password |
| `PAYSTACK_SECRET_KEY` | Found in your [Paystack Dashboard](https://dashboard.paystack.com) under Settings → API Keys |
| `DB_PASSWORD` | A strong password for the `climatewise_user` MySQL account |
| `DB_ROOT_PASSWORD` | A separate strong password for the MySQL root account (Docker only) |

---

## 🗄 Database Migrations

This project uses **Flask-Migrate** (Alembic) for schema migrations.

### First-time setup

```bash
# Only run this once if the migrations/ folder doesn't exist yet
flask db init
```

### Creating a new migration

Run this after changing any model in `app/models.py`:

```bash
flask db migrate -m "Describe what changed"
```

Always review the generated file in `migrations/versions/` before applying it.

### Applying migrations

```bash
flask db upgrade
```

### Rolling back one migration

```bash
flask db downgrade
```

### Checking current migration state

```bash
flask db current
flask db history
```

> **Production note:** Always run `flask db upgrade` after deploying a new version that includes model changes. In the Docker setup (see below), this is handled automatically by the entrypoint script.

> **MySQL note:** Make sure `PyMySQL` is listed in your `requirements.txt` and your `DATABASE_URL` uses the `mysql+pymysql://` prefix. The Docker `db` service uses a healthcheck so the `web` container won't attempt migrations until MySQL is fully ready.

---

## 💳 Paystack Integration

CYO uses [Paystack](https://paystack.com) to accept donations in Ghanaian cedis (GHS) via Mobile Money (MTN, Vodafone, AirtelTigo).

### Payment Flow

```
User fills donation form
        │
        ▼
POST /donation/initialize
  → Validates & sanitises input
  → Creates pending Donation record in DB
  → Calls Paystack API to initialize transaction
  → Redirects user to Paystack-hosted checkout page
        │
        ▼ (User completes / cancels payment on Paystack)
        │
GET /donation/callback
  → Receives reference from Paystack
  → Redirects to /donation/verify/<reference>
        │
        ▼
GET /donation/verify/<reference>
  → Verifies transaction server-side against Paystack API
  → Checks amount matches (prevents partial payment fraud)
  → Marks donation as verified in DB
  → Shows success or error flash message
        │
POST /donation/webhook  (runs in parallel, server-to-server)
  → Validates HMAC-SHA512 signature
  → Processes charge.success event
  → Marks donation verified if not already done
  → Handles cases where user closed browser before callback
```

### Setting Up Webhooks

1. Log in to your [Paystack Dashboard](https://dashboard.paystack.com)
2. Go to **Settings → Webhooks**
3. Add your webhook URL:
   ```
   https://yourdomain.com/donation/webhook
   ```
4. Paystack will POST a signed event to this URL on every completed transaction — even if the user closes their browser.

### Testing Locally

Use [ngrok](https://ngrok.com) to expose your local server for webhook testing:

```bash
ngrok http 5000
# Copy the HTTPS URL and paste it as your webhook URL in Paystack dashboard
```

Use Paystack's **Test API keys** (`sk_test_...`) and [test card/mobile numbers](https://paystack.com/docs/payments/test-payments/) during development.

### Security Notes

- The webhook endpoint verifies the `X-Paystack-Signature` header using HMAC-SHA512 before processing any event.
- Server-side verification (`/donation/verify`) always re-checks the amount received against what was stored in the database — a mismatch flags the donation as `amount_mismatch` and does not mark it verified.
- Donations are only counted in totals when `is_verified = True`.
- The Paystack reference is sanitised (`[^a-zA-Z0-9_\-]` stripped) before any database lookup.

---

## 🛡 Admin Panel

The admin panel is accessible to authenticated administrators only. It is not linked from any public page.

### Roles

| Role | Access Level |
|---|---|
| `developer` | Full access — all data, all actions |
| `ceo` | Full access — same as developer |
| `admin` | Standard access (configurable) |

An account can be disabled without deleting it by setting `is_active_account = False` in the database.

### Admin Features

| Section | Description |
|---|---|
| **Dashboard** | Live counts: volunteers, partners, unique members, verified donations total |
| **Analytics** | Chart.js — donations over time (line), volunteers vs partners (pie) |
| **Recent Activity** | Feed of latest signups, messages, and donations |
| **Volunteers** | Full list of volunteer applications with date and contact info |
| **Partners** | Full list of partner applications |
| **Donations** | All donation records with verification status, amount, and donor info |
| **Messages** | Contact form submissions |

### Creating the First Admin Account

There is no public registration for admins. Create the initial account directly in the database or via a management script:

```python
# Example: run via `flask shell`
from app import db
from app.models import Admin
from werkzeug.security import generate_password_hash

admin = Admin(
    name="Your Name",
    email="admin@climatewiseyouth.org",
    password=generate_password_hash("your-secure-password"),
    role="developer"
)
db.session.add(admin)
db.session.commit()
print("Admin created.")
```

---

## 🐳 Docker Deployment (Nginx + Gunicorn)

The production stack runs three containers orchestrated by Docker Compose:

| Container | Role |
|---|---|
| `web` | Gunicorn serving the Flask app |
| `nginx` | Reverse proxy, static files, SSL termination |
| `db` | MySQL 8 database |

### Files You Need

**`Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependency needed by PyMySQL / mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev gcc pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "wsgi:app"]
```

**`wsgi.py`**
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
```

**`docker-compose.yml`**
```yaml
version: "3.9"

services:
  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_DATABASE: climatewise_db
      MYSQL_USER: climatewise_user
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${DB_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    restart: always
    env_file: .env
    environment:
      DATABASE_URL: mysql+pymysql://climatewise_user:${DB_PASSWORD}@db:3306/climatewise_db
    depends_on:
      db:
        condition: service_healthy
    command: >
      sh -c "flask db upgrade && gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 wsgi:app"
    volumes:
      - ./static:/app/static

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./static:/app/static
      - /etc/letsencrypt:/etc/letsencrypt:ro   # For SSL certs via Certbot
    depends_on:
      - web

volumes:
  mysql_data:
```

**`nginx/nginx.conf`**
```nginx
upstream flask_app {
    server web:8000;
}

server {
    listen 80;
    server_name climatewiseyouth.org www.climatewiseyouth.org;

    # Redirect all HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name climatewiseyouth.org www.climatewiseyouth.org;

    ssl_certificate     /etc/letsencrypt/live/climatewiseyouth.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/climatewiseyouth.org/privkey.pem;

    # Serve static files directly via Nginx (faster, no Gunicorn overhead)
    location /static/ {
        alias /app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 10M;
}
```

### Deploying

```bash
# 1. Clone the repo on your server
git clone https://github.com/Saviour99/climatewise.git
cd climatewise

# 2. Set up environment variables
cp .env.example .env
nano .env   # Fill in all production values

# 3. Build and start all containers
docker compose up -d --build

# 4. Check logs
docker compose logs -f web
docker compose logs -f nginx

# 5. Obtain SSL certificate (first time only)
# Install certbot on the host, then:
sudo certbot certonly --standalone -d climatewiseyouth.org -d www.climatewiseyouth.org
docker compose restart nginx
```

### Updating the App

```bash
git pull origin main
docker compose up -d --build
```

Database migrations run automatically on container start (`flask db upgrade` is part of the startup command).

---

## 🤝 Contributing

Contributions are welcome from developers and community members alike. Please follow these steps:

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/climatewise.git
cd climatewise
```

### 2. Create a Feature Branch

Use a descriptive branch name:

```bash
git checkout -b feature/add-newsletter-subscription
git checkout -b fix/paystack-callback-edge-case
git checkout -b docs/update-deployment-guide
```

### 3. Set Up Your Local Environment

Follow the [Getting Started](#-getting-started-local-development) section above.

### 4. Make Your Changes

- Follow existing code style (PEP 8 for Python)
- Sanitise all user inputs using the utility functions in `app/utils.py`
- Do not commit `.env`, secrets, or API keys
- Write clear, descriptive commit messages

### 5. Test Your Changes

```bash
# Run the app and manually test affected pages
flask run

# If you added a new model or changed an existing one:
flask db migrate -m "your change description"
flask db upgrade
```

### 6. Open a Pull Request

Push your branch and open a PR against `main`. Include:
- A clear description of what you changed and why
- Screenshots for any UI changes
- Notes on any environment variable additions

### Code Style Guidelines

- All new routes go in `routes.py` (public) or `admin_routes.py` (admin)
- All new models go in `models.py` — always add a `__repr__` method
- All user-facing input must pass through the appropriate sanitiser in `utils.py` before use
- Use `flash()` for user feedback — never expose raw exception messages to the frontend
- Payment-related logic must always fail safe (on any error, redirect with a user-friendly message, never expose internal state)

### Reporting Bugs

Open an issue on GitHub with:
- Steps to reproduce
- Expected vs actual behaviour
- Browser / OS / Python version if relevant

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- Built and maintained by **Saviour Assandoh** — Digital Engagement & Media Lead, CYO
- Powered by [Paystack](https://paystack.com) for secure Ghana Mobile Money payments
- Hosted infrastructure by [DelaTech Consult](https://delatechconsult.com)
- Inspired by the mission of **ClimateWISE Youth Organization** — championing climate-resilient and sustainable communities across Africa

---

> _"We envision a future where every action, big or small, contributes to the well-being of people, communities, and the environment."_
> — **ClimateWISE Youth Organization**