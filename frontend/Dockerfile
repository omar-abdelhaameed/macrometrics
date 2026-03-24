# ==================== Dockerfile for React Frontend ====================
# Multi-stage build for production

# Stage 1: Builder
FROM node:20-alpine as builder

WORKDIR /app

# Copy package files first for better caching
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm ci --legacy-peer-deps

# Copy source code
COPY frontend/ ./

# Build the application
RUN npm run build


# Stage 2: Production (Nginx)
FROM nginx:alpine as production

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]