# Nuxt.js Frontend Dockerfile
# Multi-stage build for optimal image size

# Build Stage
FROM node:20-alpine as build-stage

WORKDIR /app

# Increase Node.js memory limit for SSR build
ENV NODE_OPTIONS=--max-old-space-size=2048

# Accept build arguments
# For local development, leave empty to use relative URLs
# For production, set to production API URL
ARG NUXT_PUBLIC_API_BASE=
ENV NUXT_PUBLIC_API_BASE=$NUXT_PUBLIC_API_BASE

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --legacy-peer-deps

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production Stage
FROM node:20-slim as production-stage  # <-- THE FIX IS HERE

WORKDIR /app

# Keep same Node options at runtime (safe no-op if unused)
ENV NODE_OPTIONS=--max-old-space-size=2048

# Copy package files
COPY package*.json ./

# Install only production dependencies
RUN npm ci --omit=dev --legacy-peer-deps

# Copy built application from build stage
COPY --from=build-stage /app/.output /app/.output

# Expose port 3000 (Nuxt default)
EXPOSE 3000

# Set environment to production
ENV NODE_ENV=production
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Start Nuxt server
CMD ["node", ".output/server/index.mjs"]