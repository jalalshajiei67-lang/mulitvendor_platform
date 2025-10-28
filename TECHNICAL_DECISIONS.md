# 🔧 Technical Decisions & Architecture Rationale

**Documentation of key technical decisions and their reasoning**

---

## 📋 Document Purpose

This document explains the "why" behind major technical decisions in the project, helping future developers understand the reasoning and avoid repeating past mistakes.

---

## 🏗️ Architecture Decisions

### 1. Monolithic Backend with Microservices-Ready Structure

**Decision**: Single Django project with multiple apps, but structured for potential microservices migration

**Reasoning**:
- ✅ **Simpler deployment** for MVP/initial launch
- ✅ **Shared database** reduces complexity
- ✅ **App-based structure** allows future extraction to microservices
- ✅ **Faster development** for small team
- ✅ **Easier testing** with integrated system

**Trade-offs**:
- ❌ Scaling requires scaling entire backend
- ❌ Single point of failure
- ✅ Can migrate to microservices later if needed

**Future Path**: When traffic grows, extract products/users/orders into separate services

---

### 2. Vue.js 3 with Composition API

**Decision**: Vue.js 3 with Composition API instead of Options API or React

**Reasoning**:
- ✅ **Composition API** offers better code organization
- ✅ **TypeScript-friendly** (future migration possible)
- ✅ **Smaller bundle size** than Vue 2
- ✅ **Better performance** with Proxy-based reactivity
- ✅ **Vuetify 3** provides excellent Material Design components
- ✅ **Easier to learn** than React for some developers
- ✅ **Better for Persian/RTL** support

**Alternatives Considered**:
- React: More popular, but larger ecosystem can be overwhelming
- Vue 2: Older, Options API less maintainable
- Angular: Too heavy for this use case

---

### 3. Django REST Framework (DRF) for API

**Decision**: Use DRF instead of FastAPI or plain Django

**Reasoning**:
- ✅ **Mature ecosystem** with extensive plugins
- ✅ **Built-in authentication** (Token, Session, OAuth)
- ✅ **Serializers** handle validation elegantly
- ✅ **ViewSets** reduce boilerplate code
- ✅ **Browsable API** for development
- ✅ **Excellent documentation** and community
- ✅ **Integrates perfectly** with Django ORM

**Alternatives Considered**:
- FastAPI: Faster, but less mature ecosystem
- GraphQL: Overkill for current requirements
- Plain Django: Too much boilerplate

---

### 4. PostgreSQL as Primary Database

**Decision**: PostgreSQL 15 for production, SQLite for local development

**Reasoning**:
- ✅ **Robust and reliable** for production
- ✅ **ACID compliance** ensures data integrity
- ✅ **JSON field support** for schema_markup
- ✅ **Full-text search** capability
- ✅ **Better performance** than MySQL for complex queries
- ✅ **Excellent Django support**
- ✅ **Free and open source**

**SQLite for Development**:
- ✅ Zero configuration
- ✅ File-based, easy to reset
- ✅ Good enough for development
- ✅ Matches production closely enough

---

### 5. Docker & Docker Compose

**Decision**: Containerize all services from day one

**Reasoning**:
- ✅ **Consistent environments** (dev = prod)
- ✅ **Easy onboarding** for new developers
- ✅ **Simple deployment** with compose
- ✅ **Isolated services** prevent conflicts
- ✅ **Version control** for infrastructure
- ✅ **Easy scaling** with orchestration later
- ✅ **Industry standard** for modern apps

**Configuration**:
- Production: `docker-compose.yml` (optimized)
- Local: `docker-compose.local.yml` (debug-friendly)

---

### 6. Nginx as Reverse Proxy

**Decision**: Nginx instead of Apache or direct service exposure

**Reasoning**:
- ✅ **High performance** for static files
- ✅ **Low memory footprint**
- ✅ **Excellent reverse proxy** capabilities
- ✅ **SSL/TLS termination** built-in
- ✅ **Load balancing** for future scaling
- ✅ **Gzip compression** out of box
- ✅ **Industry standard** for modern stacks

**Configuration**:
```
Nginx → Frontend (Vue.js static files)
      → Backend (/api/ → Django)
      → Media (/media/ → Shared volume)
      → Static (/static/ → Shared volume)
```

---

## 🗃️ Data Model Decisions

### 7. Three-Level Category Hierarchy

**Decision**: Department → Category → Subcategory (fixed 3 levels)

**Reasoning**:
- ✅ **Predictable structure** easier to query
- ✅ **UI/UX clarity** with fixed depth
- ✅ **Performance** - no recursive queries needed
- ✅ **Sufficient flexibility** for most e-commerce
- ✅ **Simple to understand** for non-technical users

**Example**:
```
Electronics (Department)
  └── Computers (Category)
       └── Laptops (Subcategory)
```

**Alternatives Considered**:
- Nested sets: Complex, hard to maintain
- MPTT: Overkill for fixed depth
- Unlimited nesting: Performance issues

---

### 8. Separate ProductImage Model

**Decision**: Multiple images via separate model instead of array field

**Reasoning**:
- ✅ **Better file management** with Django
- ✅ **Individual alt text** for each image
- ✅ **Ordering capability** (first image is primary)
- ✅ **Easy to add metadata** per image
- ✅ **Database normalization** best practice
- ✅ **Easier to query** and filter

**Schema**:
```python
Product (1) ----< (many) ProductImage
```

---

### 9. Token + Session Authentication

**Decision**: Use both Token and Session authentication

**Reasoning**:
- ✅ **Token** for API (frontend ↔ backend)
- ✅ **Session** for Django admin panel
- ✅ **Flexibility** for different clients
- ✅ **Standard DRF** approach
- ✅ **Easy to extend** to OAuth later

**Token Usage**:
```javascript
// Frontend stores token
localStorage.setItem('authToken', token);
// Sends with requests
headers: { Authorization: `Token ${token}` }
```

---

### 10. Slug-Based URLs for SEO

**Decision**: Use slugs for all public-facing URLs

**Reasoning**:
- ✅ **SEO-friendly** URLs
- ✅ **Human-readable** links
- ✅ **Better sharing** on social media
- ✅ **Standard practice** for content sites
- ✅ **Automatic generation** from titles

**Examples**:
```
/products/gaming-laptop-asus-rog/  # Good
/products/12345/                   # Bad
```

---

## 🎨 Frontend Architecture

### 11. Vite as Build Tool

**Decision**: Vite instead of Webpack or Vue CLI

**Reasoning**:
- ✅ **Extremely fast** dev server with HMR
- ✅ **Lightning-fast builds**
- ✅ **ES modules** native support
- ✅ **Modern tool** with great DX
- ✅ **Vue 3 officially recommends** it
- ✅ **Simple configuration**

**Performance**:
- Dev server starts: <1 second
- Hot reload: Instant
- Production build: ~30 seconds

---

### 12. Pinia for State Management

**Decision**: Pinia instead of Vuex

**Reasoning**:
- ✅ **Official recommendation** for Vue 3
- ✅ **Simpler API** than Vuex
- ✅ **TypeScript support** built-in
- ✅ **Better DevTools** integration
- ✅ **Composition API** friendly
- ✅ **Smaller bundle size**

**When NOT to use Pinia**:
- Currently using for auth state
- Could use Composition API for simpler cases
- Good for shared state across components

---

### 13. Axios for HTTP Requests

**Decision**: Axios instead of Fetch API

**Reasoning**:
- ✅ **Better error handling** out of box
- ✅ **Request/response interceptors**
- ✅ **Automatic JSON** transformation
- ✅ **Request cancellation** support
- ✅ **Timeout handling** built-in
- ✅ **Backwards compatible** with older browsers
- ✅ **Widely used** and tested

**Configuration**:
```javascript
// Centralized API client
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000
});
```

---

### 14. Vuetify for UI Components

**Decision**: Vuetify 3 instead of custom components or other libraries

**Reasoning**:
- ✅ **Material Design** out of box
- ✅ **80+ components** ready to use
- ✅ **Responsive by default**
- ✅ **Theming system** for customization
- ✅ **RTL support** for Persian
- ✅ **Accessibility** features built-in
- ✅ **Active development** and community

**Alternatives Considered**:
- Quasar: Good, but Vuetify more popular
- Element Plus: Less Material Design
- Custom: Too time-consuming

---

## 🔐 Security Decisions

### 15. Environment Variables for Secrets

**Decision**: Use .env files, never commit secrets

**Reasoning**:
- ✅ **Security best practice**
- ✅ **Different values** per environment
- ✅ **Easy to rotate** credentials
- ✅ **Standard approach** in DevOps
- ✅ **Prevents accidental** exposure

**Critical Variables**:
```env
SECRET_KEY          # Django secret
DB_PASSWORD         # Database password
DEBUG               # Debug mode flag
ALLOWED_HOSTS       # Security setting
```

---

### 16. CORS Configuration

**Decision**: Strict CORS in production, permissive in development

**Reasoning**:
- ✅ **Security** - prevents unauthorized access
- ✅ **Flexibility** - allow specific origins
- ✅ **Development ease** - allow all locally

**Configuration**:
```python
# Production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ['https://yourdomain.com']

# Development
CORS_ALLOW_ALL_ORIGINS = True
```

---

### 17. File Upload Security

**Decision**: Serve uploaded files through Nginx, not Django

**Reasoning**:
- ✅ **Performance** - Nginx serves files faster
- ✅ **Scalability** - offload from Django
- ✅ **Security** - Nginx handles path traversal
- ✅ **Caching** - Nginx can cache media

**Configuration**:
```nginx
location /media/ {
    alias /var/www/media/;
    expires 1y;
}
```

---

## 🚀 DevOps Decisions

### 18. Gunicorn as WSGI Server

**Decision**: Gunicorn instead of uWSGI or mod_wsgi

**Reasoning**:
- ✅ **Simple configuration**
- ✅ **Reliable and stable**
- ✅ **Good performance** for Python apps
- ✅ **Works well** with Nginx
- ✅ **Easy to monitor**
- ✅ **Django recommended**

**Configuration**:
```bash
gunicorn multivendor_platform.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 60
```

---

### 19. Health Checks for All Services

**Decision**: Implement health checks for Docker services

**Reasoning**:
- ✅ **Automatic recovery** from failures
- ✅ **Proper startup** sequencing
- ✅ **Monitoring integration**
- ✅ **Production reliability**

**Implementation**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/"]
  interval: 30s
  timeout: 10s
  retries: 3
```

---

### 20. Volume Persistence for Data

**Decision**: Use named volumes for database and media files

**Reasoning**:
- ✅ **Data survives** container restarts
- ✅ **Backup-friendly** named volumes
- ✅ **Performance** better than bind mounts
- ✅ **Portable** across environments

**Volumes**:
- `postgres_data` - Database persistence
- `media_files` - User uploads
- `static_files` - Static assets

---

## 📊 Performance Decisions

### 21. Pagination for List Endpoints

**Decision**: Paginate all list endpoints (10 items per page)

**Reasoning**:
- ✅ **Faster response** times
- ✅ **Lower memory** usage
- ✅ **Better UX** with progressive loading
- ✅ **Scalable** as data grows

**Configuration**:
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

---

### 22. Lazy Loading Images (Frontend)

**Decision**: Implement lazy loading for product images

**Reasoning**:
- ✅ **Faster initial load**
- ✅ **Saves bandwidth**
- ✅ **Better perceived** performance
- ✅ **Native browser** support available

**Implementation**:
```html
<img :src="product.image" loading="lazy" />
```

---

### 23. Static File Handling

**Decision**: Collect static files, serve via Nginx

**Reasoning**:
- ✅ **Performance** - Nginx faster than Django
- ✅ **Caching** - Nginx caches effectively
- ✅ **CDN-ready** - easy to add CDN later
- ✅ **Standard practice** for production

**Workflow**:
```bash
# Build phase
python manage.py collectstatic --noinput
# Runtime: Nginx serves from /static/
```

---

## 🧪 Testing Decisions

### 24. Local Docker Environment for Testing

**Decision**: Create separate docker-compose.local.yml

**Reasoning**:
- ✅ **Test before deploy** in production-like environment
- ✅ **Catch issues** early
- ✅ **Debug mode** enabled for development
- ✅ **Exposed ports** for easy access
- ✅ **Matches production** closely

**Usage**:
```bash
docker-compose -f docker-compose.local.yml up
```

---

## 📝 Documentation Decisions

### 25. Extensive Markdown Documentation

**Decision**: 40+ documentation files instead of wiki or external docs

**Reasoning**:
- ✅ **Version controlled** with code
- ✅ **Always in sync** with codebase
- ✅ **Offline access** for developers
- ✅ **Easy to update** via Git
- ✅ **Searchable** with code search
- ✅ **Portable** - lives with project

**Structure**:
- README.md - Main overview
- Guides - Step-by-step instructions
- Reference - Quick lookups
- Troubleshooting - Problem solving

---

## 🔮 Future-Proofing Decisions

### 26. RESTful API Design

**Decision**: Follow REST principles strictly

**Reasoning**:
- ✅ **Standard approach** widely understood
- ✅ **Cacheable** by nature
- ✅ **Stateless** for scalability
- ✅ **Version-able** for API evolution
- ✅ **Multiple clients** can consume

**Endpoint Structure**:
```
GET    /api/products/          # List
GET    /api/products/{id}/     # Detail
POST   /api/products/          # Create
PUT    /api/products/{id}/     # Update
DELETE /api/products/{id}/     # Delete
```

---

### 27. Internationalization (i18n) Ready

**Decision**: Use Vue I18n, even though currently Persian/English only

**Reasoning**:
- ✅ **Easy to add** more languages later
- ✅ **Better code organization**
- ✅ **RTL support** built-in
- ✅ **Industry standard** approach

**Future Languages**:
- Persian (Farsi) ✅
- English ✅
- Arabic (future)
- Turkish (future)

---

### 28. API Versioning Strategy (Planned)

**Decision**: URL-based versioning when API v2 is needed

**Reasoning**:
- ✅ **Clear separation** of versions
- ✅ **Both versions** can run simultaneously
- ✅ **Gradual migration** for clients
- ✅ **Standard practice**

**Future Structure**:
```
/api/v1/products/  # Current
/api/v2/products/  # Future
```

---

## ❌ Decisions We Avoided

### Why NOT GraphQL?
- Too complex for current requirements
- REST is sufficient and well-understood
- Smaller team, less overhead
- Can add later if needed

### Why NOT Microservices Now?
- Premature optimization
- Added complexity
- Harder to deploy and debug
- Monolith works fine for current scale

### Why NOT Redis Cache Yet?
- Database performs well currently
- Added infrastructure complexity
- Will add when needed (metrics-driven)

### Why NOT TypeScript?
- Team comfort with JavaScript
- Can migrate incrementally later
- Vue 3 works great with JS
- Type safety via prop validation

### Why NOT Kubernetes?
- Overkill for single VPS
- Docker Compose sufficient
- Can migrate when scaling up
- CapRover simpler for now

---

## 📊 Decision Impact Assessment

### High Impact, High Confidence ✅
- Django + DRF (backend framework)
- Vue.js 3 (frontend framework)
- PostgreSQL (database)
- Docker (containerization)

### High Impact, Medium Confidence ⚠️
- Three-level categories (may need adjustment)
- Token authentication (may add OAuth)

### Medium Impact, High Confidence ✅
- Vuetify (UI components)
- Vite (build tool)
- Nginx (reverse proxy)

### Low Impact, Reversible 🔄
- Pinia (could use Composition API directly)
- Pagination size (easily adjustable)

---

## 🔄 Review Schedule

This document should be reviewed and updated:
- [ ] After major architecture changes
- [ ] Every 6 months
- [ ] When adding new team members
- [ ] When technical debt accumulates

---

## 📞 Questions About These Decisions?

If you're questioning any decision:
1. Read the reasoning above
2. Check if requirements have changed
3. Measure current performance
4. Propose alternative with pros/cons
5. Discuss with team before changing

---

**Remember**: These decisions were made with specific constraints (time, budget, team size, requirements). As constraints change, decisions may need revisiting.

**Last Updated**: October 27, 2025  
**Next Review**: April 2026

