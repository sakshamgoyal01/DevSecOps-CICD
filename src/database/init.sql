-- Create user if not exists
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_user') THEN
      CREATE USER app_user WITH PASSWORD 'postgres';
   END IF;
END
$$;

-- Create database owned by app_user
CREATE DATABASE people_db OWNER app_user;

-- Connect to database
\c people_db;

-- Create table
CREATE TABLE IF NOT EXISTS public.people (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INT NOT NULL
);

-- Permissions
GRANT ALL PRIVILEGES ON TABLE public.people TO app_user;
GRANT ALL PRIVILEGES ON SEQUENCE people_id_seq TO app_user;
