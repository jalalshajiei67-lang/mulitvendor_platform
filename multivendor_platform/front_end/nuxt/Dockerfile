# Nuxt.js Frontend Dockerfile - Alternative solution
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

# Keep same Node options at runtime
ENV NODE_OPTIONS=--max-old-space-size=2048

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN rm -rf node_modules package-lock.json && \
    npm install --omit=dev --legacy-peer-deps --force

# Copy built application from build stage
COPY --from=build-stage /app/.output /app/.output

EXPOSE 3000

ENV NODE_ENV=production
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1


# ... (other commands)

# Debug: List the contents of the output directory
RUN ls -la /app/.output || true

# The command to run the application
CMD ["node", ".output/server/index.mjs"]


CMD ["node", ".output/server/index.mjs"]