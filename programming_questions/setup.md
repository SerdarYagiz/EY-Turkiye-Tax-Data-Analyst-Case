# Database Setup

This document describes how to create the PostgreSQL database environment using Docker and initialize it with the required schema.

## 1. Create PostgreSQL Docker Container

Run the following command to start a PostgreSQL container:

```bash
docker run -d \
  --name postgres-db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  postgres:16
```

Then run the **db_creation_script.sql** into the database server
