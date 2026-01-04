# ---------- Build Stage ----------
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY src/frontend/frontend/package.json src/frontend/frontend/package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source code
COPY src/frontend/frontend/ .

# Build Vite app (output: dist/)
RUN npm run build


# ---------- Runtime Stage ----------
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built frontend files
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
