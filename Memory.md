# AI Memory Document - Memory.md

This document serves as the persistent state memory for AI coding assistants working on the **Shake & Burp** project. It outlines the current state of development, active configurations, and next tasks.

---

## 1. Project Overview

- **Project Name:** Shake & Burp
- **Product:** Custom UV DTF print premium shaker bottle ecommerce platform.
- **Current Phase:** Phase 2 (Authentication & User Profiles)
- **Completion Percentage:** ~15% (Phase 1 Project setup & baseline infrastructure completed)

---

## 2. Codebase Summary & Current State

### Completed Features
- Finalized foundational docs (`PRD.md`, `Architecture.md`, `Design.md`, `Rules.md`, `Phases.md`).
- Initialized local Django 5.x project shell and set up modular apps architecture in `apps/`.
- Configured PostgreSQL 15, Redis 7, Celery 5.x, Gunicorn, and Nginx.
- Dockerized the local stack via Docker Compose running cleanly on macOS.
- Created custom `User` auth model and completed baseline database migrations.
- Set up local welcome route displaying system status metrics at port `8080`.

### Pending Features
- Phase 2: Sign-up, Sign-in with Email & Password.
- Phase 2: Google OAuth 2.0 social authentication.
- Phase 2: User profile editing and address records.
- Phase 3: Product database tables and catalog listings.
- Phase 4: Session-based and synced shopping carts.
- Phase 5: Payment integrations (Stripe/Razorpay webhook setups).
- Phase 6: Order dispatch pipelines and invoicing.
- Phase 7: Interactive client-side UV DTF customize canvas.
- Phase 8: SMTP notifications via SES + Celery.
- Phase 9: Admin dashboard analytics.
- Phase 10: Production deployment scripts and testing.

---

## 3. Tech Stack & Integration Details

- **Backend Framework:** Django (Python 3.13+)
- **Database:** PostgreSQL 15
- **Frontend Stack:** Django templates, Tailwind CSS, Vanilla JS.
- **Asynchronous Task Queue:** Redis + Celery
- **Hosting Environments:** Docker + Docker Compose, Nginx (local port `8080`), Gunicorn
- **Payment Providers:** Stripe, Razorpay
- **Email Dispatch:** Amazon SES
- **Logging & Errors:** Sentry

---

## 4. Current Folder Structure

```
Shake&Burp/
├── .agent/                 # Custom IDE agent configurations & skills
├── apps/                   # Pluggable Django applications
│   ├── accounts/           # User model & auth logic
│   ├── api/
│   ├── cart/
│   ├── core/
│   ├── dashboard/
│   ├── orders/
│   ├── payments/
│   ├── products/
│   └── wishlist/
├── config/                 # Core settings and routings
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── docker/                 # Container environments
│   ├── django.Dockerfile
│   └── nginx.conf
├── static/                 # Static styles & js
├── templates/              # HTML layout elements
├── requirements.txt        # Backend dependencies
├── docker-compose.yml      # Services configurations
├── PRD.md
├── Architecture.md
├── Design.md
├── Rules.md
├── Phases.md
└── Memory.md               # Active AI State Memory (this file)
```

---

## 5. Environment Settings & Variables

Active environment variables in `.env`:
- `DEBUG=True`
- `SECRET_KEY=django-insecure-shake-and-burp-key-change-in-prod`
- `ALLOWED_HOSTS=localhost,127.0.0.1,web`
- `DATABASE_URL=postgres://postgres:postgres@db:5432/shakeandburp`
- `REDIS_URL=redis://redis:6379/0`

---

## 6. Coding Standards & Constraints

- **Rules Enforcement:** Defined in `Rules.md`. Enforces zero-placeholders, strict type-hinting, Black formatting, Ruff checks, and mobile-first accessibility.
- **Git Flow:** Feature branching (`feat/`, `fix/`, `docs/`) and Conventional Commits (`feat:`, `fix:`, `refactor:`) are mandatory.

---

## 7. Next Recommended Tasks

1. Create a `feat/accounts-auth` branch.
2. Install `django-allauth` and other authentication dependencies.
3. Define the detailed login/register views and custom address profile forms.
4. Style form UI templates based on the dark premium aesthetic defined in `Design.md`.
