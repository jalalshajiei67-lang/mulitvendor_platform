# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Overview

This repo contains a full multivendor e‑commerce platform:
- **Backend**: Django 4 + Django REST Framework, PostgreSQL in production (SQLite allowed in dev).
- **Frontend (SPA)**: Vue 3 + Vite + Vuetify 3 + Pinia in `multivendor_platform/front_end`.
- **Frontend (Nuxt)**: A Nuxt 3 app in `multivendor_platform/front_end/nuxt` for newer flows (e.g. supplier dashboard onboarding tour).
- **DevOps**: Docker/Docker Compose for local and server deployments, CapRover on a VPS, and GitHub Actions CI/CD.

Key high‑level docs you can lean on for additional context:
- Root `README.md`: production Docker deployment & server management.
- `PROJECT_QUICK_REFERENCE.md`: one‑page cheat sheet for stack, key commands, and paths.
- `PROJECT_STRUCTURE_VISUAL.md`: architecture diagrams for backend apps, frontend layers, and API structure.
- Local dev/testing: `README_LOCAL_SETUP.md`, `RUN_LOCALLY.md`, `README_LOCAL_TESTING.md`, `TESTING_GUIDE.md`, `TEST_LOCALLY.md`, `QUICK_START_LOCAL_TESTING.md`.
- Domain guides for major subsystems: `USER_SYSTEM_GUIDE.md`, `SUPPLIER_SYSTEM_GUIDE.md`, `STRUCTURE_UPDATE.md`, and `multivendor_platform/front_end/src/stores/MIGRATION_GUIDE.md`.

## How to run the project locally

### Option A – Local Docker dev environment (recommended)

Local Docker dev uses `docker-compose.local.yml` and helper scripts.

**Linux/macOS (scripts + Compose)**
- From repo root:
  - Start all dev services (backend, frontend, DB) and set up `.env.local`:
    ```bash
    ./run-local.sh
    ```
  - Check logs:
    ```bash
    docker-compose -f docker-compose.local.yml logs -f
    ```
  - Stop services:
    ```bash
    docker-compose -f docker-compose.local.yml down
    ```
  - Stop and reset all local data, then rebuild:
    ```bash
    docker-compose -f docker-compose.local.yml down -v
    ./run-local.sh
    ```

**What this stack exposes (once healthy):**
- Frontend SPA: `http://localhost:8080`
- Backend API: `http://localhost:8000/api/`
- Django admin: `http://localhost:8000/admin/`
- PostgreSQL: `localhost:5432`

**Common container‑based backend commands**
- Create superuser:
  ```bash
  docker exec -it multivendor_backend_local python manage.py createsuperuser
  ```
- Run migrations manually:
  ```bash
  docker exec -it multivendor_backend_local python manage.py migrate
  ```
- Basic health check (backend + DB wiring):
  ```bash
  docker exec multivendor_backend_local python manage.py check
  ```

**Windows local Docker testing helpers** (mainly for human operators but useful context)
- Batch scripts (in repo root) wrap the same `docker-compose.local.yml`:
  - `test-local.bat` / `test-local-background.bat` – start stack.
  - `stop-local.bat` – stop stack.
  - `view-logs.bat` – tail logs.
  - See `README_LOCAL_TESTING.md`, `QUICK_START_LOCAL_TESTING.md`, `TEST_LOCALLY.md` for exact flows.

### Option B – Run backend & frontend without Docker

This mirrors `RUN_LOCALLY.md` and `PROJECT_QUICK_REFERENCE.md`.

**Backend (Django)**
- From repo root:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

  cd multivendor_platform/multivendor_platform
  python manage.py migrate
  python manage.py runserver
  ```
- Backend dev server: `http://127.0.0.1:8000` (API under `/api/`, admin under `/admin/`).

**Frontend SPA (Vue 3 + Vite)**
- From repo root:
  ```bash
  cd multivendor_platform/front_end
  npm install
  npm run dev
  ```
- Vite dev server (by default): `http://localhost:5173`.

**Nuxt app (where applicable)**
- For the Nuxt frontend in `multivendor_platform/front_end/nuxt`:
  ```bash
  cd multivendor_platform/front_end/nuxt
  npm install
  npm run dev
  ```
- Nuxt dev server: `http://localhost:3000` by default.

### Docker‑based production & server tooling

Root `README.md` documents the production deployment toolchain for a Django + Vue + Nginx stack (separate from CapRover flows):
- One‑command deployment (Linux/macOS):
  ```bash
  ./deploy-one-command.sh
  ```
- Step‑by‑step deploy:
  ```bash
  cp .env.production .env
  chmod +x *.sh
  ./deploy.sh
  ```
- On the VPS (after syncing code):
  ```bash
  ssh root@<server-ip>
  cd /opt/multivendor_platform
  ./server-deploy.sh
  ```
- Ongoing management (on the server):
  ```bash
  ./manage-deployment.sh          # TUI wrapper
  ./health-check.sh               # quick health
  docker-compose logs -f          # logs
  docker-compose restart          # restart services
  ./backup-database.sh            # backups
  ./update-app.sh                 # deploy updated app
  ```

CapRover + CI/CD flows are covered in `QUICK_START.md` and related docs (e.g. `CAPROVER_DEPLOYMENT_GUIDE.md`, `GITHUB_SECRETS_SETUP.md`). Use those when editing deployment definitions or CI.

## Testing

### Integration / end‑to‑end style checks (Docker)

The project’s testing docs focus on verifying that DB, backend, and frontend are wired correctly.

**Linux/macOS (local Docker stack)**
- Bring up the local stack for testing:
  ```bash
  docker-compose -f docker-compose.local.yml up --build
  ```
- Manual checks from `TESTING_GUIDE.md`:
  - DB ready:
    ```bash
    docker exec multivendor_db_local pg_isready -U postgres
    ```
  - Backend health (including DB connectivity):
    ```bash
    docker exec multivendor_backend_local python manage.py check
    ```
  - Frontend→backend connectivity (from frontend container):
    ```bash
    docker exec multivendor_frontend_local wget -qO- http://backend:80/api/products/
    ```

**Windows helpers**
- `TESTING_GUIDE.md`, `TEST_LOCALLY.md`, and `QUICK_START_LOCAL_TESTING.md` describe a `test-simple.ps1` script and other PowerShell commands that:
  - Hit `http://localhost:8000/api/products/`.
  - Hit `http://localhost:8080/`.
  - Verify DB readiness via `pg_isready`.

### Django unit tests

If you need to run Django tests directly:
- Inside the backend container:
  ```bash
  docker exec -it multivendor_backend_local python manage.py test
  ```
- Run a **single Django test case or method** (pattern standard to Django):
  ```bash
  docker exec -it multivendor_backend_local \
    python manage.py test app_name.tests.TestClass.test_method
  ```
- When running without Docker, run the same `python manage.py test ...` commands from `multivendor_platform/multivendor_platform` with the virtualenv activated.

## Frontend build, lint, and structure

### SPA in `multivendor_platform/front_end`

From that directory:
- Install deps:
  ```bash
  npm install
  ```
- Dev server:
  ```bash
  npm run dev
  ```
- Production build:
  ```bash
  npm run build
  ```
- Preview production build:
  ```bash
  npm run preview
  ```
- Lint:
  ```bash
  npm run lint
  ```

The SPA follows the architecture summarized in `PROJECT_STRUCTURE_VISUAL.md`:
- **Views**: Page‑level components (home, product list/detail/form, department/category/subcategory views, supplier pages, blog, auth, dashboards).
- **Components**: Reusable UI (layout, admin widgets, RFQ form, editor, etc.).
- **Stores (Pinia)**: Auth, products, blog and modularized domain stores in `src/stores/modules` (departments, categories, subcategories, products, orders). `MIGRATION_GUIDE.md` explains how the old monolithic `products.js` was split and how to import from the new index.
- **Services**: `src/services/api.js` centralizes Axios configuration and API calls.
- **Plugins**: Vuetify, i18n (Persian/RTL), and others.
- **Routing**: Vue Router defines the main site map (auth, product catalog, suppliers, blog, dashboards).

### Nuxt app in `multivendor_platform/front_end/nuxt`

This codebase uses a Nuxt 3 app for newer UX (e.g. the supplier onboarding tour described in `onboarding-tour-verify.md`). From that directory:
- Dev server:
  ```bash
  npm run dev
  ```
- Production build & preview:
  ```bash
  npm run build
  npm run preview
  ```

Nuxt is used for more complex flows (like multi‑step tours) while still talking to the same Django API.

## Backend architecture

Summarized from `PROJECT_STRUCTURE_VISUAL.md`, `USER_SYSTEM_GUIDE.md`, and `SUPPLIER_SYSTEM_GUIDE.md`.

### High‑level backend layout

Backend root: `multivendor_platform/multivendor_platform`.
- Django project config in `multivendor_platform/` (settings, `urls.py`, `wsgi.py`).
- Core apps:
  - `users/`: auth, profiles, roles (buyer/seller/both/admin), dashboards, ads, activity logging.
  - `products/`: departments, categories, subcategories, products, images, reviews, scraper.
  - `orders/`: orders, items, RFQs, payments.
  - `blog/`: posts, categories, comments.
  - Shared `media/`, `static/`, and `templates/` folders.

Data model highlights:
- Users: Django `auth_user` extended via `UserProfile`, `BuyerProfile`, `VendorProfile`, and `Supplier` entities, plus `UserActivity` for auditing.
- Products: hierarchical Department → Category → Subcategory → Product, with multiple images and reviews.
- Orders: `Order` (supports RFQ), `OrderItem`, `OrderImage`, and `Payment`.
- Blog: `BlogCategory`, `BlogPost`, `BlogComment`.

`STRUCTURE_UPDATE.md` documents that subcategories now infer their departments via categories (instead of a direct M2M to departments). Serializers expose departments as a computed field; the admin and forms have been simplified accordingly.

### API surface

The REST API is namespaced under `/api/` and roughly organized as:
- `/api/auth/…` – authentication and role‑based dashboards (buyer/seller/admin), profile update, admin user management, activity logs.
- `/api/products/…` – product CRUD, hierarchical taxonomy (departments/categories/subcategories), and per‑user product views.
- `/api/orders/…` – order and RFQ creation, vendor/admin RFQ management.
- `/api/blog/…` – blog posts, categories, comments.
- `/api/users/suppliers/…` and `/api/users/supplier-comments/…` – supplier listing, detail, products, comments, and commenting endpoints as detailed in `SUPPLIER_SYSTEM_GUIDE.md`.

## Major domain flows

These docs give deep, cross‑file context:

- `USER_SYSTEM_GUIDE.md` – user system & dashboards
  - Defines roles (Buyer, Seller, Both, Admin) and their dashboards.
  - Explains models (`UserProfile`, `BuyerProfile`, `VendorProfile`, `SellerAd`, `ProductReview`, `UserActivity`).
  - Lists key auth and dashboard endpoints.
  - Describes frontend dashboards (buyer, seller, admin) and role‑based routing.

- `SUPPLIER_SYSTEM_GUIDE.md` – supplier directory & comments
  - Backend: extended `VendorProfile` fields, `SupplierComment` model, new serializers and viewsets.
  - API endpoints for supplier listing, detail, products, comments, and posting comments.
  - Frontend: `/suppliers` (grid listing) and `/suppliers/:id` (tabbed detail view) pages, integrated into navigation (header, drawer, footer).

- `multivendor_platform/front_end/src/stores/MIGRATION_GUIDE.md` – product taxonomy stores
  - Explains the split of the old `products.js` Pinia store into specialized module stores for departments, categories, subcategories, products, and orders.
  - Provides patterns for cross‑store flows, e.g. loading hierarchical data and mapping URL slugs to entities.

- `multivendor_platform/front_end/nuxt/tests/onboarding-tour-verify.md` – supplier onboarding tour
  - Documents a 20‑step guided onboarding tour for the supplier dashboard, implemented with `driver.js`, `useSupplierOnboarding.ts`, and multiple `data-tour` attributes across dashboard, product form, and mini‑website components.
  - Describes UX constraints (simple Persian copy, large fonts, RTL, mobile‑friendly) and how progress/persistence work via localStorage.

## Style and implementation rules (from .cursorrules)

When generating or editing code, align with the Cursor rules file where they are project‑specific:

### Backend (Python/Django)
- Use Django REST Framework conventions with **class‑based views** and **serializers**.
- Follow PEP 8 and Django naming conventions (models `PascalCase`, fields `snake_case`).
- Use type hints where practical (Python 3.9+).
- Design RESTful endpoints with appropriate HTTP verbs and status codes.
- Keep queries efficient (prefer `select_related` / `prefetch_related` to avoid N+1 issues) and paginate list endpoints.

### Frontend (Vue/Vuetify)
- Use **Vue 3 Composition API**, **ES6+**, and **Pinia** for state management.
- Prefer **async/await** over raw promise chains.
- Use **Vuetify 3** components for UI and follow the Vue style guide.
- Naming:
  - `camelCase` for variables and functions.
  - `PascalCase` for components.

### UX and language requirements
- **Design must be mobile‑first**.
- **Design must be RTL**.
- **All UX copy should be in Persian**.

These are strict project‑specific rules: when adding or modifying UI, defer to these constraints.

## Where to look before making non‑trivial changes

- For architecture or domain questions: `PROJECT_STRUCTURE_VISUAL.md`, `PROJECT_QUICK_REFERENCE.md`, `USER_SYSTEM_GUIDE.md`, `SUPPLIER_SYSTEM_GUIDE.md`.
- For taxonomy and product‑related UX/logic: `STRUCTURE_UPDATE.md` and the Pinia `MIGRATION_GUIDE.md`.
- For local environments and debugging connection issues: `README_LOCAL_SETUP.md`, `RUN_LOCALLY.md`, `READMЕ_LOCAL_TESTING.md`, `TESTING_GUIDE.md`, `TEST_LOCALLY.md`, `QUICK_START_LOCAL_TESTING.md`.
- For deployment/CI changes: root `README.md`, `QUICK_START.md`, `CAPROVER_*` and `GITHUB_*` docs.

Use these docs as primary sources so that new code and configuration stay aligned with the existing architecture and operational flows.