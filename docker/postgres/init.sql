-- PostgreSQL initialization script for Genesis Backend
-- Creates necessary databases and users for development and testing

-- Create development database if it doesn't exist
SELECT 'CREATE DATABASE genesis_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'genesis_db')\gexec

-- Create test database if it doesn't exist
SELECT 'CREATE DATABASE genesis_test_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'genesis_test_db')\gexec

-- Connect to development database
\c genesis_db;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create schema for genesis backend
CREATE SCHEMA IF NOT EXISTS genesis;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA genesis TO genesis;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA genesis TO genesis;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA genesis TO genesis;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA genesis GRANT ALL ON TABLES TO genesis;
ALTER DEFAULT PRIVILEGES IN SCHEMA genesis GRANT ALL ON SEQUENCES TO genesis;

-- Connect to test database and repeat
\c genesis_test_db;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

CREATE SCHEMA IF NOT EXISTS genesis;

GRANT ALL PRIVILEGES ON SCHEMA genesis TO genesis;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA genesis TO genesis;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA genesis TO genesis;

ALTER DEFAULT PRIVILEGES IN SCHEMA genesis GRANT ALL ON TABLES TO genesis;
ALTER DEFAULT PRIVILEGES IN SCHEMA genesis GRANT ALL ON SEQUENCES TO genesis;

-- Sample tables for testing (optional)
CREATE TABLE IF NOT EXISTS genesis.sample_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO genesis.sample_users (email, name) VALUES 
    ('test@example.com', 'Test User'),
    ('admin@example.com', 'Admin User')
ON CONFLICT (email) DO NOTHING;

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'Genesis Backend PostgreSQL initialization completed successfully';
END $$;
