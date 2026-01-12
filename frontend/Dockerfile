# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ .

# Build for production
RUN npm run build -- --configuration=production

# Production stage
FROM nginx:alpine

# Copy custom nginx config template
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf.template

# Copy built application from build stage
COPY --from=build /app/dist/frontend /usr/share/nginx/html

# Create startup script
RUN echo '#!/bin/sh\n\
PORT=${PORT:-80}\n\
sed "s/\${PORT}/$PORT/g" /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf\n\
nginx -g "daemon off;"\n\
' > /start.sh && chmod +x /start.sh

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx with PORT substitution
CMD ["/start.sh"]
