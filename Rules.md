# Coding Standards and AI Constraints - Rules.md

This document defines the strict development standards, system constraints, security policies, and architectural rules for the **Shake & Burp** project. **All developers and AI assistants must adhere to these instructions without exception.**

---

## 1. General Rules

- **Zero Placeholder Code:** Never write `// TODO: implement`, `pass`, or placeholder variables. Write full, functional, production-ready logic.
- **No Pseudo-Code:** All generated code snippets must be executable and complete.
- **Follow DRY (Don't Repeat Yourself):** Extract common logic into modular helper functions or abstract model classes.
- **SOLID Design Principles:** Enforce single responsibility, open-closed, Liskov substitution, interface segregation, and dependency inversion.
- **KISS (Keep It Simple, Stupid):** Avoid over-engineering. Write clean, readable logic before complex micro-optimizations.
- **Clean Architecture & Django Best Practices:** Keep models thin, views focused, and delegate complex business rules to separate service layers or helper modules.

---

## 2. Python & Backend Rules

- **Python Version:** Target **Python 3.13+**. Use modern language features (e.g., advanced typing, structural pattern matching).
- **Database Interaction:** Use the **Django ORM exclusively** for database queries. Never write raw SQL statements unless running performance-critical database operations that are fully covered by tests and reviews.
- **Strict Type Hints:** Every function signature, method parameter, and return value must include precise Python type hints.
- **Formatting & Linting:**
  - Formatting is enforced via **Black** style configurations.
  - Linting, complexity checks, and code quality imports sorting are managed via **Ruff**.
- **Secret Management:** Never hardcode passwords, secret keys, API tokens, or webhook signatures. Retrieve values exclusively from environmental variables using `os.environ` or `django-environ`.

---

## 3. Database Rules

- **Database Engine:** Target **PostgreSQL** exclusively.
- **Database Schema Constraints:**
  - Every model relationship must utilize explicit `ForeignKey` constraints with defined deletion actions (`on_delete=models.PROTECT` or `on_delete=models.CASCADE`).
  - Add explicit database indexes (`db_index=True` or `indexes` in model `Meta`) for fields that are queried frequently (e.g., slugs, email fields, transaction status).
  - Enforce data integrity with constraints (e.g., `UniqueConstraint`, `CheckConstraint`).
- **Database Transactions:** Group database operations that write to multiple models (e.g., creating an order and charging a payment) within a `transaction.atomic()` block to prevent orphan records or partial writes.

---

## 4. Frontend & Styling Rules

- **Stack Constraints:**
  - Frontend code consists of standard **Django HTML templates**, styled with **Tailwind CSS** utility classes, and interactive behavior driven by **Vanilla JavaScript**.
  - **No SPA Frameworks:** Do not introduce React, Vue, Angular, or Svelte frameworks to run the client application.
  - **React Bits Exception:** React Bits components are utilized only as isolated background animations. They must be included using custom pre-compiled bundles loaded via CDN/scripts, keeping the core site logic written in Vanilla JS.
- **Styling Direction:**
  - Implement layouts using **Mobile-First** responsive practices (Tailwind `@media` breakpoints: `sm`, `md`, `lg`, `xl`).
  - Follow accessible structural patterns (use semantic HTML5 tags: `<main>`, `<section>`, `<nav>`, `<article>`, `<header>`, `<footer>`).

---

## 5. Security Rules

- **CSRF Protection:** Ensure the standard Django CSRF middleware is enabled. Every POST/PUT form must contain a `{% csrf_token %}` template tag.
- **XSS Prevention:** Trust Django’s template engine to auto-escape values. Avoid mark_safe() or standard raw filter usage unless the variable content is explicitly validated and cleaned using a sanitization library.
- **SQL Injection:** Avoid interpolating variables directly inside raw queries. Let the Django ORM handle param validation automatically.
- **Rate Limiting:** Implement limits on high-frequency endpoints (e.g., login, password resets, file upload customizer APIs) via Django middleware or Redis-based rate limiters.
- **Cookie Security:** Enforce secure cookies:
  ```python
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  SESSION_COOKIE_HTTPONLY = True
  ```
- **Content Security Policy (CSP):** Configure security middleware headers to restrict script executions to trusted domains and pre-approved CDNs only.

---

## 6. Docker Containerization Rules

- **Multi-Stage Builds:** Dockerfiles must split builder steps from runner environments to keep images lightweight.
- **Minimal Image Footprint:** Base images must use alpine or debian-slim variants.
- **Non-Root Execution:** Create a dedicated non-root application user (`django`) in the Dockerfile and launch the container processes using it. Never run application services inside containers as `root`.

---

## 7. AWS Cloud Services Rules

- **Media & File Storage:** S3 is used for media, custom design uploads, and static assets. Always set ACLs to private for sensitive documents (invoices, receipts).
- **Transactional Emails:** All system-generated emails must go through Amazon SES. SPF, DKIM, and DMARC records must be verified.
- **RDS Database:** PostgreSQL must run on AWS RDS with Multi-AZ redundancy enabled, located in a private VPC subnet.

---

## 8. Version Control (Git) Rules

- **Feature Branching:** Never commit changes directly to the `main` branch. Perform changes on isolated branch names following:
  - `feat/feature-name` (New additions)
  - `fix/bug-name` (Fixes)
  - `docs/documentation-changes` (Docs)
- **Conventional Commits:** Commit messages must follow structured prefixes:
  - `feat: add customizer decal scaling functionality`
  - `fix: resolve Stripe webhook signature validation crash`
  - `refactor: optimize DB query in accounts dashboard`

---

## 9. Testing & Quality Gates

- **Unit Tests:** Every custom helper, form, and validation class must have comprehensive unit tests.
- **Integration Tests:** Cover standard endpoint flows (e.g., add to cart -> checkout -> success page). Ensure API endpoints return appropriate status codes.
- **End-to-End Tests:** Automate checkout sequences and visualizer flows using testing frameworks (e.g., Playwright).

---

## 10. Documentation Rules

- **Code Comments:** Every function, class, and custom model field must contain descriptive docstrings detailing parameters, return types, and exceptions raised.
- **API Documentation:** Expose up-to-date documentation for custom visualizer APIs, including request schemas and return formats.

---

## 11. Strict AI Restrictions

As an AI Assistant, you are strictly **FORBIDDEN** from doing the following:
- **Inventing APIs:** Never use backend or frontend APIs that do not exist or are not imported.
- **Inventing Libraries:** Only use packages declared in `requirements.txt`. Do not install packages without verifying their production viability.
- **Ignoring Errors:** Do not swallow exceptions in empty `except:` blocks. Always log errors via `logger.exception()` and surface helpful feedback to the user.
- **Removing Tests:** Never delete existing test assertions or suites unless refactoring obsolete logic.
- **Bypassing Security:** Do not write bypass mechanisms for authentication, CSRF validation, or rate limiters.
- **Breaking Folder Structure:** Respect the established pluggable apps architecture. Place views, forms, and services inside the respective modular directories.
- **Using Deprecated Modules:** Verify API status. Never use deprecated packages or methods.

**Always explain why a design decision is made when writing or editing code.**
