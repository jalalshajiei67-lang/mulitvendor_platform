# Build stage
FROM node:20-alpine as build-stage

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies with legacy peer deps for compatibility
RUN npm ci --legacy-peer-deps --prefer-offline

# Copy project configuration
COPY vite.config.js jsconfig.json index.html ./

# Copy source code and public assets
COPY src ./src
COPY public ./public

# Set production environment
ENV NODE_ENV=production

# Build the app with increased memory and verbose logging
RUN NODE_OPTIONS="--max-old-space-size=4096" npm run build -- --logLevel info

# Production stage
FROM nginx:alpine as production-stage

# Copy built files to nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

