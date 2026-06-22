-- Retail Inventory AI Agent — Full Schema
-- Combines all migrations in dependency order

CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

SOURCE migrations/001_create_products.sql;
SOURCE migrations/002_create_stock.sql;
SOURCE migrations/003_create_sales.sql;