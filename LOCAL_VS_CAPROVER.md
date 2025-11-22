# Local Development vs CapRover Deployment

## 📋 Overview

| Aspect | Local Development | CapRover Production |
|--------|------------------|---------------------|
| **Orchestration** | Docker Compose | CapRover Dashboard |
| **Database** | Docker container | CapRover One-Click App |
| **Redis** | Docker container | CapRover One-Click App |
| **Backend** | Docker + Hot reload | CapRover App (Daphne) |
| **Frontend** | Docker + Hot reload | CapRover App (Nuxt SSR) |
| **HTTPS** | Not configured | Automatic Let's Encrypt |
| **Domain** | localhost | indexo.ir |
| **Deployment** | `docker-compose up` | Git push (CI/CD) |

## 🚀 Local Development

### Files Used
- `docker-compose.yml` - Multi-container setup
- `.env` - Local environment variables
- `Dockerfile` - Backend image
- `multivendor_platform/front_end/nuxt/Dockerfile` - Frontend image

### Start Local Environment
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Access Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Development Features
- ✅ Hot reload for code changes
- ✅ Debug mode enabled
- ✅ All CORS origins allowed
- ✅ Direct database access
- ✅ Volume mounts for live editing

## 🌐 CapRover Production

### Architecture
```
Your Code (GitHub)
    ↓ (Push to main)
GitHub Actions
    ↓ (Deploy)
CapRover Server (185.208.172.76)
    ├── multivendor-backend (Daphne + Django)
    ├── multivendor-frontend (Nuxt SSR)
    ├── multivendor-db (PostgreSQL)
    └── multivendor-redis (Redis)
```

### Files Used
- `captain-definition` - Backend deployment config
- `Dockerfile` - Backend production image
- `multivendor_platform/front_end/nuxt/captain-definition` - Frontend deployment config
- `multivendor_platform/front_end/nuxt/Dockerfile` - Frontend production image
- `.github/workflows/deploy-caprover.yml` - CI/CD pipeline

### Deployment Process
1. **Push code** to GitHub main branch
2. **GitHub Actions** automatically triggers
3. **Builds** Docker images
4. **Deploys** to CapRover
5. **CapRover** manages containers, SSL, domains

### Access Services
- **Frontend**: https://indexo.ir
- **Backend API**: https://api.indexo.ir (or multivendor-backend.indexo.ir)
- **Admin**: https://api.indexo.ir/admin

### Production Features
- ✅ HTTPS with automatic SSL
- ✅ Custom domains
- ✅ Zero-downtime deployments
- ✅ Automatic container restart
- ✅ Persistent data volumes
- ✅ Environment variable management
- ✅ Centralized logging

## 🔄 Workflow

### Typical Development Cycle
```
1. Code locally with docker-compose
2. Test features on localhost
3. Commit changes to Git
4. Push to main branch
5. GitHub Actions deploys to CapRover
6. Verify on production (indexo.ir)
```

### Environment Variables

#### Local (.env)
```env
DEBUG=True
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

#### CapRover (App Settings)
```env
DEBUG=False
DB_HOST=srv-captain--multivendor-db
DB_PORT=5432
ALLOWED_HOSTS=indexo.ir,www.indexo.ir,api.indexo.ir
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
```

## 🎯 Key Differences

### Docker Compose (Local)
- **Purpose**: Local development
- **Configuration**: `docker-compose.yml`
- **Services**: All in one file
- **Networking**: Docker bridge network
- **Volumes**: Local file mounts
- **SSL**: No HTTPS
- **Updates**: Manual (`docker-compose up --build`)

### CapRover (Production)
- **Purpose**: Production deployment
- **Configuration**: Individual app configs
- **Services**: Separate CapRover apps
- **Networking**: CapRover internal network
- **Volumes**: Persistent CapRover volumes
- **SSL**: Automatic Let's Encrypt
- **Updates**: Automatic via GitHub Actions

## 📝 Best Practices

### Local Development
1. Use `docker-compose.yml` for consistency
2. Keep `.env` file for local secrets
3. Use hot reload for faster development
4. Test with DEBUG=True

### Production (CapRover)
1. Never commit secrets to Git
2. Use CapRover environment variables
3. Always use HTTPS
4. Set DEBUG=False
5. Use strong database passwords
6. Enable app tokens for CI/CD

## 🔧 Troubleshooting

### Local Issues
```bash
# Reset everything
docker-compose down -v
docker-compose up --build -d

# View logs
docker-compose logs backend
docker-compose logs frontend

# Access backend shell
docker-compose exec backend bash
```

### CapRover Issues
1. Check CapRover app logs
2. Verify environment variables
3. Check GitHub Actions logs
4. Restart app if needed
5. Check domain DNS settings

## 🚫 What NOT to Use for CapRover

- ❌ Don't use `docker-compose.yml` for CapRover deployment
- ❌ Don't use Nginx container (CapRover provides routing)
- ❌ Don't manually manage SSL certificates
- ❌ Don't expose database ports publicly

## ✅ Summary

- **Local**: Use `docker-compose.yml` for development
- **Production**: Use CapRover with GitHub Actions CI/CD
- **Both**: Share the same `Dockerfile` but different configs
- **Separation**: Keep local and production concerns separate


