-- MySQL initialization script for Genesis Backend
-- Creates necessary databases, tables, and sample data

-- Create test database
CREATE DATABASE IF NOT EXISTS genesis_test_db;

-- Grant permissions to genesis user
GRANT ALL PRIVILEGES ON genesis_db.* TO 'genesis'@'%';
GRANT ALL PRIVILEGES ON genesis_test_db.* TO 'genesis'@'%';
FLUSH PRIVILEGES;

-- Use the main database
USE genesis_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    password_hash VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_users_email (email),
    INDEX idx_users_active (is_active),
    INDEX idx_users_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    avatar_url VARCHAR(500),
    bio TEXT,
    phone VARCHAR(20),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_profiles_user (user_id),
    INDEX idx_profiles_name (first_name, last_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_roles_name (name),
    INDEX idx_roles_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create user_roles junction table
CREATE TABLE IF NOT EXISTS user_roles (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    role_id CHAR(36) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by CHAR(36),
    expires_at TIMESTAMP NULL,
    
    UNIQUE KEY unique_user_role (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_roles_user (user_id),
    INDEX idx_user_roles_role (role_id),
    INDEX idx_user_roles_expires (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2),
    sku VARCHAR(100) UNIQUE,
    category VARCHAR(100),
    tags JSON,
    stock_quantity INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    images JSON,
    specifications JSON,
    weight DECIMAL(8,2),
    dimensions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_products_name (name),
    INDEX idx_products_category (category),
    INDEX idx_products_price (price),
    INDEX idx_products_sku (sku),
    INDEX idx_products_active (is_active),
    INDEX idx_products_stock (stock_quantity),
    FULLTEXT idx_products_search (name, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    shipping_amount DECIMAL(10,2) DEFAULT 0.00,
    payment_method VARCHAR(50),
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    shipping_address JSON,
    billing_address JSON,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    shipped_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_orders_user (user_id),
    INDEX idx_orders_status (status),
    INDEX idx_orders_payment_status (payment_status),
    INDEX idx_orders_number (order_number),
    INDEX idx_orders_created (created_at),
    INDEX idx_orders_total (total_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    order_id CHAR(36) NOT NULL,
    product_id CHAR(36) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_sku VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_order_items_order (order_id),
    INDEX idx_order_items_product (product_id),
    INDEX idx_order_items_quantity (quantity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create audit_log table for tracking changes
CREATE TABLE IF NOT EXISTS audit_log (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    table_name VARCHAR(100) NOT NULL,
    record_id CHAR(36) NOT NULL,
    action ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    old_values JSON,
    new_values JSON,
    user_id CHAR(36),
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_audit_table (table_name),
    INDEX idx_audit_record (record_id),
    INDEX idx_audit_action (action),
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample roles
INSERT INTO roles (name, description, permissions) VALUES
('admin', 'System Administrator', JSON_ARRAY('all')),
('manager', 'Manager Role', JSON_ARRAY('users.read', 'users.write', 'products.read', 'products.write', 'orders.read')),
('user', 'Regular User', JSON_ARRAY('products.read', 'orders.read', 'profile.write'))
ON DUPLICATE KEY UPDATE description = VALUES(description);

-- Insert sample users
INSERT INTO users (email, name, password_hash) VALUES
('admin@genesis.dev', 'Genesis Admin', '$2b$12$hashed_password_here'),
('manager@genesis.dev', 'Genesis Manager', '$2b$12$hashed_password_here'),
('user@genesis.dev', 'Test User', '$2b$12$hashed_password_here')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Get user IDs for role assignment
SET @admin_id = (SELECT id FROM users WHERE email = 'admin@genesis.dev');
SET @manager_id = (SELECT id FROM users WHERE email = 'manager@genesis.dev');
SET @user_id = (SELECT id FROM users WHERE email = 'user@genesis.dev');

SET @admin_role_id = (SELECT id FROM roles WHERE name = 'admin');
SET @manager_role_id = (SELECT id FROM roles WHERE name = 'manager');
SET @user_role_id = (SELECT id FROM roles WHERE name = 'user');

-- Assign roles to users
INSERT INTO user_roles (user_id, role_id, assigned_by) VALUES
(@admin_id, @admin_role_id, @admin_id),
(@manager_id, @manager_role_id, @admin_id),
(@user_id, @user_role_id, @admin_id)
ON DUPLICATE KEY UPDATE assigned_at = CURRENT_TIMESTAMP;

-- Insert sample user profiles
INSERT INTO user_profiles (user_id, first_name, last_name, bio) VALUES
(@admin_id, 'Genesis', 'Admin', 'System administrator for Genesis Backend'),
(@manager_id, 'Genesis', 'Manager', 'Manager for Genesis Backend'),
(@user_id, 'Test', 'User', 'Regular user for testing purposes')
ON DUPLICATE KEY UPDATE bio = VALUES(bio);

-- Insert sample products
INSERT INTO products (name, description, price, cost, sku, category, stock_quantity, specifications) VALUES
('Sample Product 1', 'High-quality sample product for testing', 29.99, 15.00, 'SKU-001', 'electronics', 100, JSON_OBJECT('weight', '1kg', 'color', 'black')),
('Sample Product 2', 'Another great sample product', 49.99, 25.00, 'SKU-002', 'clothing', 50, JSON_OBJECT('size', 'M', 'material', 'cotton')),
('Sample Product 3', 'Premium sample product', 99.99, 50.00, 'SKU-003', 'home', 25, JSON_OBJECT('dimensions', '30x20x10cm', 'material', 'wood'))
ON DUPLICATE KEY UPDATE description = VALUES(description);

-- Insert sample order
SET @sample_product_id = (SELECT id FROM products WHERE sku = 'SKU-001' LIMIT 1);

INSERT INTO orders (user_id, order_number, total_amount, shipping_address) VALUES
(@user_id, 'ORD-001', 29.99, JSON_OBJECT('street', '123 Test St', 'city', 'Test City', 'state', 'TS', 'zipCode', '12345'))
ON DUPLICATE KEY UPDATE total_amount = VALUES(total_amount);

SET @sample_order_id = (SELECT id FROM orders WHERE order_number = 'ORD-001');

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price, product_name, product_sku) VALUES
(@sample_order_id, @sample_product_id, 1, 29.99, 29.99, 'Sample Product 1', 'SKU-001')
ON DUPLICATE KEY UPDATE quantity = VALUES(quantity);

-- Create same structure in test database
USE genesis_test_db;

-- Copy table structures to test database (without data)
CREATE TABLE users LIKE genesis_db.users;
CREATE TABLE user_profiles LIKE genesis_db.user_profiles;
CREATE TABLE roles LIKE genesis_db.roles;
CREATE TABLE user_roles LIKE genesis_db.user_roles;
CREATE TABLE products LIKE genesis_db.products;
CREATE TABLE orders LIKE genesis_db.orders;
CREATE TABLE order_items LIKE genesis_db.order_items;
CREATE TABLE audit_log LIKE genesis_db.audit_log;

-- Add foreign key constraints to test database
ALTER TABLE user_profiles ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE user_roles ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE user_roles ADD FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE;
ALTER TABLE user_roles ADD FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE orders ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT;
ALTER TABLE order_items ADD FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE;
ALTER TABLE order_items ADD FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT;
ALTER TABLE audit_log ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;

-- Log successful initialization
SELECT 'Genesis Backend MySQL initialization completed successfully' AS message;
