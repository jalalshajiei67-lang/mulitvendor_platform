# 📁 Project Structure

This document describes the clean, organized structure of the multivendor platform project.

## Root Directory Structure

```
/ (Project Root)
├── docker-compose.yml       # Production Docker Compose configuration
├── docker-compose.local.yml # Local Development Docker Compose configuration
├── deploy.sh                # Deployment automation script
├── .env                     # Local secrets (GitIgnored - DO NOT COMMIT!)
├── .github/
│   └── workflows/
│       └── docker-deploy.yml # CI/CD GitHub Actions workflow
├── nginx/                   # Nginx configuration folder
│   └── nginx.conf          # Main Nginx configuration file
└── [other project files...]
```

## File Descriptions

### Docker Configuration
- **`docker-compose.yml`**: Production environment configuration
  - Uses production settings
  - Includes all services (db, redis, backend, frontend, traefik, nginx)
  - Configured for VPS deployment

- **`docker-compose.local.yml`**: Local development configuration
  - Uses development settings (DEBUG=True)
  - Simplified setup for local testing
  - Exposes ports for local access

### Deployment
- **`deploy.sh`**: Automated deployment script
  - Builds Docker images
  - Starts services
  - Runs migrations
  - Collects static files
  - Performs health checks

### CI/CD
- **`.github/workflows/docker-deploy.yml`**: GitHub Actions workflow
  - Triggers on push to `main` branch
  - SSH to VPS and executes deployment
  - Automated CI/CD pipeline

### Nginx
- **`nginx/nginx.conf`**: Main Nginx configuration
  - Static file serving
  - Media file serving
  - Gzip compression
  - Logging configuration

### Environment
- **`.env`**: Local environment variables (GitIgnored)
  - Database credentials
  - Django secret key
  - API keys and secrets
  - **⚠️ NEVER commit this file!**

## Usage

### Local Development
```bash
docker compose -f docker-compose.local.yml up --build
```

### Production Deployment
```bash
# Manual deployment
bash deploy.sh

# Or via GitHub Actions (automatic on push to main)
git push origin main
```

## Notes

- All sensitive files (`.env`) are in `.gitignore`
- Production and local configurations are separated
- CI/CD is automated via GitHub Actions
- Nginx configuration is centralized in `nginx/` folder
