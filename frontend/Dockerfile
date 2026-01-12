# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copy entire project to build context
COPY . .

# Install dependencies from frontend package
RUN cd frontend && npm ci

# Build for production
RUN cd frontend && npm run build -- --configuration=production

# List the build output to verify
RUN ls -la frontend/dist/

# Production stage
FROM nginx:alpine

# Remove default nginx files
RUN rm -rf /usr/share/nginx/html/*

# Copy built application from build stage
COPY --from=build /app/frontend/dist/frontend /usr/share/nginx/html

# Verify files were copied
RUN ls -la /usr/share/nginx/html/

# Copy nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
