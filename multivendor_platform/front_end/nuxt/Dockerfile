FROM node:20-slim AS build-stage

WORKDIR /app

# Increase Node.js memory limit for SSR build
ENV NODE_OPTIONS=--max-old-space-size=2048

# Accept build arguments
ARG NUXT_PUBLIC_API_BASE=""
ENV NUXT_PUBLIC_API_BASE=$NUXT_PUBLIC_API_BASE

# Copy package files
COPY package*.json ./

# Clear any cached data and install with rebuild
RUN rm -rf node_modules package-lock.json && \
    npm install --legacy-peer-deps --force && \
    npm rebuild

# Copy source code
COPY . .

# Build the application with a fallback
RUN npm run build || npm run build

# Production Stage
FROM node:20-slim AS production-stage

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Keep same Node options at runtime
ENV NODE_OPTIONS=--max-old-space-size=2048

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN rm -rf node_modules package-lock.json && \
    npm install --omit=dev --legacy-peer-deps --force

# Copy built application from build stage
COPY --from=build-stage /app/.output /app/.output

# Debug: List the contents of the output directory
RUN ls -la /app/.output || true

EXPOSE 3000

ENV NODE_ENV=production
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

# Health check using curl instead of wget
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Start the application
CMD ["node", ".output/server/index.mjs"]