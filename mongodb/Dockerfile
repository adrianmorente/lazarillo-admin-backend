# Reuse mongo image just to copy initialization script
FROM mongo:latest

# Adds init script that is run automatically by mongo image
ADD init-user.js /docker-entrypoint-initdb.d
