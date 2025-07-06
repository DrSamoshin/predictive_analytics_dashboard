FROM postgres:16-alpine

# Set environment variables for database initialization
ENV POSTGRES_DB=instagram_analytics
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Copy initialization scripts if needed
# COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432 