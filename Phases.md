# Project Roadmap and Phases - Phases.md

This document outlines the detailed development phases for the **Shake & Burp** ecommerce platform. Each phase is designed to be self-contained and detailed enough for autonomous execution.

---

## Phase 1: Project Setup & Baseline Infrastructure

### Objectives
Initialize the development environment, version control, containerization pipelines, and database baselines.

### Features
- Standard skeleton layout for pluggable Django applications.
- Docker Compose configuration for multi-container orchestration.
- Basic linting/formatting rules pre-configured.

### Tasks
- Initialize git repository and create branch protection rules.
- Set up Django 5.x project under `config/` directory.
- Create container configurations (`docker/django.Dockerfile`, `docker/nginx.conf`, `docker-compose.yml`).
- Configure environment isolation with `.env.example`.
- Setup standard requirements files.

### Dependencies
None.

### Deliverables
- Functional local Docker environment running Django, PostgreSQL, Redis, and Nginx.
- Validated database connections.

### Testing
- Run Django system check: `docker-compose exec web python manage.py check`.
- Verify database migrations run cleanly: `docker-compose exec web python manage.py migrate`.

### Completion Checklist
- [ ] Docker containers build and run without errors.
- [ ] Django welcome page is accessible at `localhost:80` through Nginx.
- [ ] Ruff and Black check passes.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/setup-infrastructure`
- **Git Milestone:** `Milestone 1: Project Initialization`
- **Pull Request Name:** `feat: initialize Django, Docker, Postgres, and Nginx environment`
- **Docker Image Name:** `shake-web:phase-1`
- **GitHub Release:** `v0.1.0-alpha`
- **Suggested Documentation:** `README.md` containing installation, environment setup, and docker build guidelines.

---

## Phase 2: Authentication & User Profiles

### Objectives
Establish secure user registration, profiles, email verification, and OAuth integrations.

### Features
- Standard email/password signup and login.
- Google OAuth 2.0 social login.
- Secure password recovery workflow.
- User profile dashboard.

### Tasks
- Extend `AbstractUser` to create `User` and `Profile` models in `apps.accounts`.
- Set up Django Authentication URLs and forms (custom styled with Tailwind).
- Integrate `django-allauth` for Google social authentication.
- Create user dashboard views, allowing address changes and avatar uploads.

### Dependencies
- **Phase 1** infrastructure.

### Deliverables
- Functional user registration, login, and social sign-in endpoints.
- User profile updates views.

### Testing
- Write unit tests for login and registration forms.
- Verify Google OAuth redirects to correct callback.

### Completion Checklist
- [ ] Users can sign up and login with email/password.
- [ ] Users can sign up and login with Google OAuth.
- [ ] Session cookies are set with secure headers.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/accounts-auth`
- **Git Milestone:** `Milestone 2: Authentication`
- **Pull Request Name:** `feat: implement secure authentication and profile management`
- **Docker Image Name:** `shake-web:phase-2`
- **GitHub Release:** `v0.2.0-alpha`
- **Suggested Documentation:** User accounts model definitions in database diagrams.

---

## Phase 3: Product Catalog & Inventory Management

### Objectives
Implement base shaker models, color options, ready-made decal structures, and inventory trackers.

### Features
- Shaker bottle category filter.
- Product grid with color variants.
- Product detail pages displaying technical specs and stock availability.
- UV DTF ready-made decal library.

### Tasks
- Implement models `Product`, `Category`, `ProductImage`, `BottleColor`, and `Decal` in `apps.products`.
- Set up Django admin screens for base products and color variations.
- Build clean catalog template views.
- Write search and tag filtering views.

### Dependencies
- **Phase 2** for profile connections on product wishlist operations.

### Deliverables
- Completed database tables for catalog data.
- User-facing pages for product listings and details.

### Testing
- Test database schemas and unique field constraints.
- Test category filters and database search query performance.

### Completion Checklist
- [ ] Base shakers, colors, and stock levels are editable via Django admin.
- [ ] Product details display correct variant images depending on color selection.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/catalog-inventory`
- **Git Milestone:** `Milestone 3: Product Catalog`
- **Pull Request Name:** `feat: create product database models, views, and catalog templates`
- **Docker Image Name:** `shake-web:phase-3`
- **GitHub Release:** `v0.3.0-alpha`
- **Suggested Documentation:** Detailed model specifications in `docs/products_schema.md`.

---

## Phase 4: Cart, Wishlist, and Checkout Layout

### Objectives
Implement session-based and db-synced cart behaviors, wishlists, and checkout routing.

### Features
- Dynamic slide-out cart drawer.
- Wishlist toggles.
- Consolidated single-page checkout form.

### Tasks
- Build `apps.cart` and `apps.wishlist` models and view controllers.
- Write logic to merge anonymous session cart with user database cart upon login.
- Implement checkout form templates collecting shipping addresses.
- Write discount coupon validation backend.

### Dependencies
- **Phase 3** catalog models.

### Deliverables
- Session and DB cart syncing system.
- Complete checkout visual layout with address capture.

### Testing
- Unit test cart addition, modification, and subtraction methods.
- Test coupon validation for expiration dates, double-use, and minimum spend values.

### Completion Checklist
- [ ] Anonymous users can add products to cart and maintain items across visits.
- [ ] Cart correctly merges with database items upon login.
- [ ] Checkout page calculates correct item totals.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/cart-checkout`
- **Git Milestone:** `Milestone 4: Cart & Checkout`
- **Pull Request Name:** `feat: implement cart drawer, wishlist, and checkout views`
- **Docker Image Name:** `shake-web:phase-4`
- **GitHub Release:** `v0.4.0-alpha`

---

## Phase 5: Payment Gateway Integration

### Objectives
Integrate Stripe and Razorpay checkout APIs and configure webhook transaction verification.

### Features
- Multi-currency payment execution.
- Transaction validation and logging.
- Auto-refund logic for cancelled sessions.

### Tasks
- Configure Stripe and Razorpay SDK inside `apps.payments`.
- Implement payment authorization creation views.
- Write secure webhook handlers checking stripe signatures and Razorpay HMAC hashes.
- Store results in `PaymentTransaction` tables.

### Dependencies
- **Phase 4** checkout logic.

### Deliverables
- Payment modal interfaces.
- Webhook endpoints listening for success events.

### Testing
- Simulate successful payments using Stripe CLI webhook triggers.
- Verify signature validations reject modified payloads.

### Completion Checklist
- [ ] Orders transition from `PENDING` to `PAID` upon verified webhook trigger.
- [ ] Failed payments log transaction reports.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/payment-integrations`
- **Git Milestone:** `Milestone 5: Payment Systems`
- **Pull Request Name:** `feat: integrate Stripe and Razorpay payment gateways`
- **Docker Image Name:** `shake-web:phase-5`
- **GitHub Release:** `v0.5.0-alpha`

---

## Phase 6: Order Pipeline & Fulfillment

### Objectives
Implement order dispatch flows, invoice processing, and shipping tracking updates.

### Features
- Invoicing and PDF receipts.
- Shipping tracking updates.
- Admin custom order fulfillment dashboard.

### Tasks
- Code status states transitions inside `apps.orders` views.
- Implement PDF invoice generator.
- Integrate third-party shipping APIs to fetch tracking numbers.
- Dispatch status updates to customer profile page.

### Dependencies
- **Phase 5** payment webhooks.

### Deliverables
- PDF invoice download routes.
- Tracking verification inputs.

### Testing
- Unit test status changes triggers.
- Verify PDF compiles correctly.

### Completion Checklist
- [ ] Invoices compile correct details.
- [ ] Status updates write to database logs.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/order-fulfillment`
- **Git Milestone:** `Milestone 6: Orders & Shipments`
- **Pull Request Name:** `feat: build order pipeline and automatic invoicing`
- **Docker Image Name:** `shake-web:phase-6`
- **GitHub Release:** `v0.6.0-alpha`

---

## Phase 7: Interactive UV DTF Customizer

### Objectives
Build the core client-side 2D design customizer and save design coordinates for printing.

### Features
- High-fidelity visualizer canvas.
- SVG/PNG image uploads with dimensions check.
- Canvas coordinate calculations.

### Tasks
- Write custom HTML5 Canvas/Vanilla JS customizations wrapper in `static/js/customizer.js`.
- Add controls: scale, rotate, drag, layer.
- Set up API upload endpoint mapping file keys to `Customization` models.
- Build Admin customization details screen displaying overlays coordinates.

### Dependencies
- **Phase 3** decal libraries.

### Deliverables
- Active UI customizer canvas.
- Print data API serialization.

### Testing
- Test upload parameters constraints.
- Verify canvas coordinate calculations return correct offsets.

### Completion Checklist
- [ ] Users can drag decals onto canvas.
- [ ] Admin dashboard renders layout with correct coordinates.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/customizer-canvas`
- **Git Milestone:** `Milestone 7: Customization Visualizer`
- **Pull Request Name:** `feat: create customizer HTML5 canvas and print asset downloader`
- **Docker Image Name:** `shake-web:phase-7`
- **GitHub Release:** `v0.7.0-alpha`

---

## Phase 8: Emails & Notifications

### Objectives
Configure Amazon SES and Celery tasks for async transactional email dispatches.

### Features
- Async welcome emails.
- Async order invoice notifications.
- Shipping status dispatch updates.

### Tasks
- Integrate `django-ses` connection settings.
- Implement Celery tasks calling standard templates.
- Configure queue triggers on database status alterations.

### Dependencies
- **Phase 6** orders and Phase 1 Celery infrastructure.

### Deliverables
- Queue notification workers.
- Transactional email HTML designs.

### Testing
- Verify emails write to console during development.
- Monitor Celery worker execution logs.

### Completion Checklist
- [ ] Emails dispatch asynchronously.
- [ ] Check links verify successfully.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/notifications-ses`
- **Git Milestone:** `Milestone 8: Transactions Emails`
- **Pull Request Name:** `feat: build transactional email notifications using Amazon SES`
- **Docker Image Name:** `shake-web:phase-8`
- **GitHub Release:** `v0.8.0-alpha`

---

## Phase 9: Admin Dashboard & Content Management

### Objectives
Establish custom admin statistics dashboards and static page layout CMS controllers.

### Features
- Interactive statistics dashboard.
- CMS interface for Blogs, FAQs, and Banners.

### Tasks
- Build custom layout controllers in `apps.dashboard`.
- Render charts using Chart.js.
- Create content controllers for FAQ/Banners database items.

### Dependencies
- **Phase 6** order datasets.

### Deliverables
- Admin-only analytics pages.
- Dynamic FAQs views.

### Testing
- Restrict dashboard URLs from standard clients.
- Verify CRUD forms submit valid parameters.

### Completion Checklist
- [ ] Analytics graphs render correct metrics.
- [ ] FAQs edit correctly without server errors.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/admin-dashboard`
- **Git Milestone:** `Milestone 9: Admin Dashboard`
- **Pull Request Name:** `feat: add custom admin panel dashboard and CMS controls`
- **Docker Image Name:** `shake-web:phase-9`
- **GitHub Release:** `v0.9.0-alpha`

---

## Phase 10: Performance, SEO, Security Hardening & Deployment

### Objectives
Optimize assets cache parameters, configure security headers, and deploy setup to AWS.

### Features
- Security headers configurations.
- Production cache parameters.
- Rolling deployments pipelines.

### Tasks
- Run audits and configure Sentry logs reporting.
- Setup AWS EC2, Multi-AZ RDS database, and configure Cloudflare DNS.
- Set up GitHub Actions deploy hooks.

### Dependencies
All prior phases.

### Deliverables
- Live URL matching specifications.
- Monitored errors reports.

### Testing
- Run complete pytest suite.
- Audit site using Lighthouse performance suites.

### Completion Checklist
- [ ] Lighthouse audits report 95+ score.
- [ ] SSL connection validates cleanly.

### Suggested Release & Version Control Details
- **Branch Name:** `feat/prod-deployment`
- **Git Milestone:** `Milestone 10: Production Go-Live`
- **Pull Request Name:** `feat: deploy production code base on AWS EC2`
- **Docker Image Name:** `shake-web:latest`
- **GitHub Release:** `v1.0.0-gold`
