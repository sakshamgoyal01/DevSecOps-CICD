FROM postgres:15

# Environment variables (non-secret defaults for local)
ENV POSTGRES_DB=people_db
ENV POSTGRES_USER=app_user
ENV POSTGRES_PASSWORD=postgres

# Copy init script
COPY src/database/init.sql /docker-entrypoint-initdb.d/
